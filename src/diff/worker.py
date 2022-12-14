import time
import os
import socket
import uuid
import traceback
import asyncio
import nats
import json
import functools
from typing import List
from diff.config import GenConfig, NatsConfig, VideoConfig
from diff.gen import Generator
from diff.upscale import Upscaler
from diff.storage import save_image, commit, get_request, read_binary_file, save_video, get_selected_images_for_request, get_videos
from diff.messages import DiffusionTask, UpscaleTask, GenVideoTask, AddAudioTask
from diff.nats import nats_connect
from logging import info, error
from dataclasses import dataclass


def resize_img(in_file: str, out_file: str, scale: str = "512x512"):
    command = f"convert -resize {scale} {in_file} {out_file}"
    info(command)
    os.system(command)


def run_in_executor(f):

    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, lambda: f(*args, **kwargs))

    return inner


@dataclass
class Worker:
    output_dir: str
    gen_config: GenConfig
    nats_config: NatsConfig
    video_config: VideoConfig
    dry_run: bool = False
    until_done: bool = False
    task_kind: str = 'diffusion'

    def queue(self) -> str:
        return f"tasks-{self.task_kind}"

    def stream_name(self) -> str:
        return f"tasks-stream-{self.queue()}"

    def durable_name(self) -> str:
        hostname = socket.gethostname()
        return f"durable-{self.task_kind}-{hostname}"

    async def nats_connect(self):
        self.nc = await nats_connect(self.nats_config.url())

    async def diffusion_cb(self, data):
        task = DiffusionTask(**json.loads(data))
        info(f"Task in diffusion_cb: {task.json()}")
        await self.diffusion(task.request_id)

    async def upscale_cb(self, data):
        task = UpscaleTask(**json.loads(data))
        info(f"Task in upscale_cb: {task.json()}")
        await self.upscale(task.image_id)

    async def video_cb(self, data):
        task = GenVideoTask(**json.loads(data))
        info(f"Task in video_cb: {task.json()}")
        await self.make_video(task.request_id)

    async def audio_cb(self, data):
        task = AddAudioTask(**json.loads(data))
        info(f"Task in audio_cb: {task.json()}")
        await self.add_audio(task.video_id, task.file_path)

    async def loop(self):
        await self.nats_connect()
        queue = self.queue()
        js = self.nc.jetstream()

        info(f"Subscribing NATS for {queue}")
        sub = await js.pull_subscribe(subject=queue,
                                      durable=self.durable_name(),
                                      stream=self.stream_name())
        info(f"Started loop for {queue}")
        sleep_duration = 2

        while True:
            msgs = []

            try:
                msgs = await sub.fetch(1)
            except Exception as e:
                error(f"Fetch error: {e}")
                if self.until_done:
                    info(f"No tasks, running until done, quitting now!")
                    return
                info(f"Sleeping for {sleep_duration}s")
                await asyncio.sleep(sleep_duration)
                continue

            # await msg.in_progress()
            msg = msgs[0]
            if not msg._ackd:
                await msg.ack_sync()
            data = msg.data.decode()

            try:
                if self.task_kind == 'diffusion':
                    await self.diffusion_cb(data)
                if self.task_kind == 'upscale':
                    await self.upscale_cb(data)
                if self.task_kind == 'video':
                    await self.video_cb(data)
                if self.task_kind == 'audio':
                    await self.audio_cb(data)
            except Exception as e:
                error(e)
                traceback.print_exc()

    def run(self):
        if self.task_kind == 'diffusion':
            self.generator = Generator(self.gen_config.small_vram)
        if self.task_kind == 'upscale':
            self.upscaler = Upscaler()

        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.loop())
        loop.close()
        self.nc.close()

    @run_in_executor
    def diffusion(self, rid: int):
        try:
            request = get_request(rid)
            info(f"Diffusion for request#{rid} \"{request.prompt}\"")
            images = []

            if self.task_kind == 'diffusion' and self.generator:
                result = self.generator.generate(
                    request.prompt,
                    batch_size=self.gen_config.batch_size,
                    batch_count=self.gen_config.batch_count,
                    inference_steps=self.gen_config.inference_steps,
                )

                images = result.save(
                    request_id=request.id,
                    folder=self.output_dir,
                )

            for img in images:
                save_image(img, rid, 1)

            request.generated = True
        except Exception as e:
            error(e)
            traceback.print_exc()
        finally:
            commit()

    @run_in_executor
    def upscale(self, img_id: int):
        try:
            info(f"Upscale for image#{img_id}")

            if self.upscaler:
                self.upscaler.upscale(img_id=img_id)
        except Exception as e:
            error(e)
            traceback.print_exc()
        finally:
            commit()

    @run_in_executor
    def make_video(self, rid: int):
        req = get_request(rid)
        print(req)
        images = get_selected_images_for_request(req.id)
        print(f"Video generation for {rid} \"{req.prompt}\"")

        cnt = len(images)
        print(cnt)
        folder = "output/videos"
        img_folder = "output/tmp"
        os.makedirs(folder, exist_ok=True)
        os.makedirs(img_folder, exist_ok=True)

        d = " \\\n"
        out = f"{folder}/{rid}.mp4"

        loop_section = d.join(
            map(lambda i: f"-loop 1 -t 3 -i {img_folder}/{i}.png", range(cnt)))

        fpp = self.video_config.frames_per_pic

        filter_section = d.join(
            map(
                lambda i:
                f"[{i+1}]fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+{(i+1)*fpp}/TB[f{i}];",
                range(cnt - 2)))

        overlay_subsection = d.join(
            map(lambda i: f"[bg{i}][f{i}]overlay[bg{i+1}];", range(1,
                                                                   cnt - 3)))

        overlay_section = f"[0][f0]overlay[bg1];{d}{overlay_subsection}{d}[bg{cnt-3}][f{cnt-3}]overlay,format=yuv420p[v]"

        command = f"ffmpeg{d}-y{d}{loop_section}{d}-filter_complex{d}\"{filter_section}{d}{overlay_section}\"{d}-r 25{d}-map \"[v]\"{d}{out}"
        info(f"Command:\n{command}")

        for i, f in enumerate(images):
            fname = f"{img_folder}/{i}.png"
            with open(fname, 'wb') as fb:
                info(f"Writing {fname}")
                fb.write(read_binary_file(f.hqoid or f.oid))
            resize_img(fname, fname, self.video_config.scale)

        # FOR DEBUGGING
        # with open("slideshow.sh", "w") as f:
        #     f.write(command)

        os.system(command)
        save_video(out, req.id)

    @run_in_executor
    def add_audio(self, vid: int, audio_file: str):
        vid = get_videos([vid])[0]
        folder = "output/videos"
        os.makedirs(folder, exist_ok=True)
        out = f"{folder}/{uuid.uuid1()}.mp4"
        command = f"ffmpeg -i {vid.filename} -i {audio_file} -map 0:v -map 1:a -c:v copy -shortest {out}"
        info(command)

        with open(vid.filename, 'wb') as fb:
            info(f"Writing {vid.filename}")
            fb.write(read_binary_file(vid.oid))

        os.system(command)
        save_video(out, vid.request.id)

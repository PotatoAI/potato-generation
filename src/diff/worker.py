import time
import os
import socket
import uuid
import traceback
import asyncio
import nats
import json
from typing import List
from diff.config import GenConfig, NatsConfig, VideoConfig
from diff.gen import Generator
from diff.upscale import Upscaler
from diff.storage import save_image, commit, get_request, read_binary_file, save_video, get_selected_images_for_request, get_videos
from diff.messages import BaseTask, GenVideoTask, AddAudioTask
from logging import info, error
from dataclasses import dataclass


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

    async def nats_connect(self):
        info("Connecting to NATS")
        self.nc = await nats.connect(self.nats_config.url())

    async def loop(self):
        await self.nats_connect()
        queue = self.queue()
        js = self.nc.jetstream()
        await js.add_stream(name=f"tasks-stream-{queue}", subjects=[queue])

        async def base_cb(msg):
            data = msg.data.decode()
            task = BaseTask(**json.loads(data))
            info(f"Task: {task.json()}")
            try:
                if task.kind == 'diffusion':
                    self.diffusion(task.request_id)
                if task.kind == 'upscale':
                    self.upscale(task.request_id)
            except Exception as e:
                error(e)
                traceback.print_exc()
            finally:
                await msg.ack()

        async def video_cb(msg):
            data = msg.data.decode()
            task = GenVideoTask(**json.loads(data))
            info(f"Task: {task.json()}")
            try:
                self.make_video(task.request_id)
            except Exception as e:
                error(e)
                traceback.print_exc()
            finally:
                await msg.ack()

        async def audio_cb(msg):
            data = msg.data.decode()
            task = AddAudioTask(**json.loads(data))
            info(f"Task: {task.json()}")
            try:
                self.add_audio(task.video_id, task.file_path)
            except Exception as e:
                error(e)
                traceback.print_exc()
            finally:
                await msg.ack()

        if self.task_kind == 'diffusion' or self.task_kind == 'upscale':
            await js.subscribe(queue, queue, cb=base_cb)

        if self.task_kind == 'video':
            await js.subscribe(queue, queue, cb=video_cb)

        if self.task_kind == 'audio':
            await js.subscribe(queue, queue, cb=audio_cb)

        info(f"Started loop for {queue}")

    def run(self):
        if self.task_kind == 'diffusion':
            self.generator = Generator()
        if self.task_kind == 'upscale':
            self.upscaler = Upscaler()

        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.loop())
        loop.run_forever()
        loop.close()

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

    def upscale(self, rid: int):
        try:
            request = get_request(rid)
            info(f"Upscale for request#{rid} \"{request.prompt}\"")

            if self.upscaler:
                self.upscaler.upscale(rid=rid)

            request.generated = True
        except Exception as e:
            error(e)
            traceback.print_exc()
        finally:
            commit()

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

        os.system(command)
        save_video(out, req.id)

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

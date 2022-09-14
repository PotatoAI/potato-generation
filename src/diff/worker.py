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
from diff.storage import get_top_task, has_top_task, save_image, commit, get_request, read_binary_file, save_video, get_selected_images_for_request, get_videos
from diff.messages import BaseTask
from logging import info, error
from dataclasses import dataclass


@dataclass
class Worker:
    output_dir: str
    gen_config: GenConfig
    nats_config: NatsConfig
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
        await js.add_stream(name="worker-stream", subjects=[queue])

        async def cb(msg):
            data = msg.data.decode()
            task = BaseTask(**json.loads(data))
            info(f"Task: {task.json()}")
            if task.kind == 'diffusion':
                self.diffusion(task.request_id)
            if task.kind == 'upscale':
                self.upscale(task.request_id)
            await msg.ack()

        await js.subscribe(queue, f"worker-{self.task_kind}", cb=cb)
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
                    batch_size=self.config.batch_size,
                    batch_count=self.config.batch_count,
                    inference_steps=self.config.inference_steps,
                )

                images = result.save(
                    request_id=request.id,
                    task_id=1,
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
            images = []

            if self.upscaler:
                images = self.upscaler.upscale(rid=rid)

            for img in images:
                save_image(img, rid, 1)

            request.generated = True
        except Exception as e:
            error(e)
            traceback.print_exc()
        finally:
            commit()


class SlideshowWorker:

    def __init__(self, config: VideoConfig):
        self.config = config

    def run(self):
        print('yeah, sure')

    def generate(self, ids: List[int]):
        for id in ids:
            self.generate_one(id)

    def generate_one(self, id: int):
        print(f"gen for {id}")
        req = get_request(id)
        print(req)
        images = get_selected_images_for_request(req.id)
        cnt = len(images)
        print(cnt)
        folder = "output/videos"
        img_folder = "output/tmp"
        os.makedirs(folder, exist_ok=True)
        os.makedirs(img_folder, exist_ok=True)

        d = " \\\n"
        out = f"{folder}/{id}.mp4"

        loop_section = d.join(
            map(lambda i: f"-loop 1 -t 3 -i {img_folder}/{i}.png", range(cnt)))

        fpp = self.config.frames_per_pic

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
                fb.write(read_binary_file(f.oid))

        os.system(command)
        save_video(out, req.id)

    def add_audio(self, vid: List[int], metadata: List[str]):
        vids = get_videos(vid)
        audio_file = metadata[0]
        folder = "output/videos"
        os.makedirs(folder, exist_ok=True)
        for vid in vids:
            out = f"{folder}/{uuid.uuid1()}.mp4"
            command = f"ffmpeg -i {vid.filename} -i {audio_file} -map 0:v -map 1:a -c:v copy -shortest {out}"
            info(command)

            with open(vid.filename, 'wb') as fb:
                info(f"Writing {vid.filename}")
                fb.write(read_binary_file(vid.oid))

            os.system(command)
            save_video(out, vid.request.id)

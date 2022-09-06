import time
import os
import socket
import uuid
from typing import List
from diff.config import GenConfig, VideoConfig
from diff.gen import Generator
from diff.storage import get_top_task, has_top_task, save_image, commit, get_request, read_binary_file, save_video, get_selected_images_for_request, get_videos
from logging import info, error


class Worker:
    def __init__(
        self,
        output_dir: str,
        gen_config: GenConfig,
        dry_run=False,
        until_done=False,
    ):
        self.task_kind = "diffusion"
        self.output_dir = output_dir
        self.config = gen_config
        self.dry_run = dry_run
        self.until_done = until_done

    def run(self):
        gen = Generator()

        while True:
            avaliable_tasks = has_top_task(self.task_kind)
            info(f"{avaliable_tasks} Tasks in queue")

            if avaliable_tasks == 0:
                if self.until_done:
                    info("Queue is empty, exiting worker")
                    return
                info('Waiting in a loop')
                time.sleep(10)

            if not self.dry_run and avaliable_tasks > 0:
                task, request = get_top_task(self.task_kind)
                task.worker_id = socket.gethostname()
                task.running = True
                log = f"Running generator for \"{request.prompt}\" task #{task.id} -> request #{request.id}"
                info(log)
                task.log = log
                commit()

                try:

                    result = gen.generate(
                        request.prompt,
                        batch_size=self.config.batch_size,
                        batch_count=self.config.batch_count,
                        inference_steps=self.config.inference_steps,
                    )

                    images = result.save(
                        request_id=request.id,
                        task_id=task.id,
                        folder=self.output_dir,
                    )

                    for img in images:
                        save_image(img, request.id, task.id)

                    task.status = 'success'
                    request.generated = True
                except Exception as e:
                    task.status = 'error'
                    task.error = str(e)
                    error(e)
                finally:
                    task.running = False
            else:
                info('Dry Run')

            commit()


class SlideshowWorker:
    def __init__(self):
        self.frames_per_pic = 4

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

        filter_section = d.join(
            map(
                lambda i:
                f"[{i+1}]fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+{(i+1)*self.frames_per_pic}/TB[f{i}];",
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

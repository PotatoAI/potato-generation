import time
import os
import socket
from diff.config import GenConfig
from diff.gen import Generator
from diff.storage import get_top_task, has_top_task, save_image, commit, get_request, read_binary_file
from logging import info, error


class Worker:
    def __init__(
        self,
        output_dir: str,
        gen_config: GenConfig,
        dry_run=False,
    ):
        self.task_kind = "diffusion"
        self.dry_run = dry_run
        self.output_dir = output_dir
        self.config = gen_config

    def run(self):
        gen = Generator()

        while True:
            avaliable_tasks = has_top_task(self.task_kind)
            info(f"{avaliable_tasks} Tasks in queue")

            if avaliable_tasks == 0:
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
    def __init__(self, ):
        self.something = 1

    def run(self):
        print('yeah, sure')

    def generate(self):
        ids = [19]
        for id in ids:
            self.generate_one(id)

    def generate_one(self, id: int):
        print(f"gen for {id}")
        req = get_request(id)
        print(req)
        cnt = len(req.images)
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
                f"[{i+1}]fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+{(i+1)*2}/TB[f{i}];",
                range(cnt - 2)))

        overlay_subsection = d.join(
            map(lambda i: f"[bg{i}][f{i}]overlay[bg{i+1}];", range(1,
                                                                   cnt - 3)))

        overlay_section = f"[0][f0]overlay[bg1];{d}{overlay_subsection}{d}[bg{cnt-3}][f{cnt-3}]overlay,format=yuv420p[v]"

        command = f"ffmpeg{d}-y{d}{loop_section}{d}-filter_complex{d}\"{filter_section}{d}{overlay_section}\"{d}-r 25{d}-map \"[v]\"{d}{out}"
        info(f"Command:\n{command}")

        for i, f in enumerate(req.images):
            fname = f"{img_folder}/{i}.png"
            with open(fname, 'wb') as fb:
                info(f"Writing {fname}")
                fb.write(read_binary_file(f.oid))

        os.system(command)

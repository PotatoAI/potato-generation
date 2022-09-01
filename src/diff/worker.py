from os.path import join
import time
import socket
from diff.config import GenConfig
from diff.gen import Generator
from diff.storage import get_top_task, has_top_task, save_image, commit, get_request
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
        imgs_count = len(req.images)
        print(imgs_count)
        folder = "output/videos"
        img_folder = "output/tmp"
        out = f"{folder}/{id}.mp4"

        loop_section = "\n".join(
            map(lambda i: f"-loop 1 -t 3 -i {img_folder}/{i}.png",
                range(imgs_count)))

        filter_section = "\n".join(
            map(
                lambda i:
                f"[{i+1}]fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+{i+1*2}/TB[f{i}];",
                range(imgs_count - 1)))

        command = f"ffmpeg\n{loop_section}\n-filter_complex\n\"{filter_section}\"\n-r 25\n{out}"
        print(command)


# ffmpeg
# -loop 1 -t 3 -i img001.jpg
# -loop 1 -t 3 -i img002.jpg
# -loop 1 -t 3 -i img003.jpg
# -loop 1 -t 3 -i img004.jpg
# -loop 1 -t 3 -i img005.jpg
# -filter_complex
# "[1]fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+2/TB[f0];
#  [2]fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+4/TB[f1];
#  [3]fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+6/TB[f2];
#  [4]fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+8/TB[f3];
#  [0][f0]overlay[bg1];
#  [bg1][f1]overlay[bg2];
#  [bg2][f2]overlay[bg3];
#  [bg3][f3]overlay,format=yuv420p[v]"
# -map "[v]"
# -r 25
# output-crossfade.mp4

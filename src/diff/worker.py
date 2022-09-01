import time
import socket
from diff.config import GenConfig
from diff.gen import Generator
from diff.storage import get_top_task, has_top_task, save_image, commit
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
                commit()

                try:
                    log = f"Running generator for \"{request.prompt}\" task #{task.id} -> request #{request.id}"
                    info(log)
                    task.log = f"{task.log}\n{log}"

                    result = gen.generate(
                        f"request/{request.id}",
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

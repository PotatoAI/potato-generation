import time
from diff.config import GenConfig
from diff.gen import Generator
from diff.storage import get_top_task, has_top_task, save_image


class Worker:
    def __init__(
        self,
        sess,
        output_dir: str,
        gen_config: GenConfig,
        dry_run=False,
    ):
        self.sess = sess
        self.dry_run = dry_run
        self.output_dir = output_dir
        self.config = gen_config

    def run(self):
        gen = Generator()

        while True:
            print('Waiting in a loop')
            time.sleep(1)

            avaliable_tasks = has_top_task(self.sess)
            print(f"{avaliable_tasks} Tasks in queue")

            if not self.dry_run and avaliable_tasks > 0:
                task, request = get_top_task(self.sess)
                task.running = True
                self.sess.commit()

                try:
                    print(
                        f"Running generator for \"{request.prompt}\" task #{task.id} -> request #{request.id}"
                    )
                    result = gen.generate(request.prompt,
                                          cols=self.config.cols,
                                          rows=self.config.rows)
                    images = result.save(request.id, str(task.id),
                                         self.output_dir)

                    for img in images:
                        save_image(self.sess, img, request.id, task.id)

                    task.status = 'success'
                except Exception as e:
                    print(e)
                    task.error = str(e)
                    task.status = 'error'
                finally:
                    task.running = False
                    self.sess.commit()
            else:
                print('Dry Run')

import time
from diff.gen import Generator
from diff.storage import get_top_task, has_top_task


class WorkerThread:
    def __init__(self, sess, dry_run=False):
        self.sess = sess
        self.dry_run = dry_run

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
                    imgs = gen.generate(request.prompt, cols=1, rows=1)
                    print(imgs)
                    # imgs.save(args.output)
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


def start(sess, dry_run):
    t = WorkerThread(sess, dry_run)
    t.run()

import time
from diff.gen import Generator
from diff.storage import get_top_task


class WorkerThread:
    def __init__(self, sess, dry_run=False):
        self.sess = sess
        self.dry_run = dry_run

    def run(self):
        gen = Generator()

        while True:
            print('sleep')
            time.sleep(1)
            if not self.dry_run:
                task, request = get_top_task(self.sess)
                import pprint
                pprint.pprint(task)

                try:
                    print(f"Running generator for \"{request.prompt}\"")
                    imgs = gen.generate(request.prompt, cols=1, rows=1)
                    print(imgs)
                    # imgs.save(args.output)
                except Exception as e:
                    print(e)
                    task.error = str(e)

                self.sess.commit()
            else:
                print('Dry Run')


def start(sess, dry_run):
    t = WorkerThread(sess, dry_run)
    t.run()

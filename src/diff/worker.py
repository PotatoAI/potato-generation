import threading
import time
from diff.gen import Generator


class WorkerThread(threading.Thread):
    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def run(self, *args, **kwargs):
        while True:
            print('Hello')
            if not self.dry_run:
                gen = Generator()
                print(gen)
                # imgs = gen.generate(args.prompt, cols=1, rows=1)
                # imgs.save(args.output)
            else:
                print('Dry Run')
            time.sleep(1)


def start(dry_run):
    t = WorkerThread(dry_run)
    t.start()

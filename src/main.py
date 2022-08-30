from diff.login import login
import diff.db
import diff.worker
import diff.config
import diff.schema
from diff.storage import add_new_request
import argparse


def worker(args):
    print(args)
    config = diff.config.read(args.config)
    print(config)

    login(config.hf.token)
    diff.worker.start(args.dry_run)


def request(args):
    print(args)
    config = diff.config.read(args.config)
    print(config)
    sess = diff.db.session(config.db)
    add_new_request(sess, args.prompt, priority=10)


def migrate(args):
    print(args)
    config = diff.config.read(args.config)
    print(config)
    diff.db.migrate(config.db)


def repl(args):
    print(args)
    config = diff.config.read(args.config)
    print(config)
    sess = diff.db.session(config.db)
    task = diff.storage.get_top_task(sess)
    print(task.id)
    # import IPython
    # IPython.embed()


parser = argparse.ArgumentParser(description='Generate some AI stuff')

parser.add_argument('--config',
                    help='Config file path',
                    nargs='?',
                    default='config.yaml')
parser.add_argument(
    '--dry-run',
    help='Simulate generation without actually genarting anything',
    action='store_true')
parser.add_argument('--output-folder',
                    help='Prompt to use for one time generation',
                    nargs='?',
                    default='output')

subparsers = parser.add_subparsers(help='sub-command help')

parser_worker = subparsers.add_parser('worker', help='Run worker')
parser_request = subparsers.add_parser('request', help='Run prompt once')
parser_migrate = subparsers.add_parser('migrate', help='Run migrate')
parser_repl = subparsers.add_parser('repl', help='Drop into REPL')

parser_request.add_argument('--prompt',
                            help='Prompt to schedule a task',
                            nargs='?',
                            default='Cute cat')

parser_worker.set_defaults(func=worker)
parser_request.set_defaults(func=request)
parser_migrate.set_defaults(func=migrate)
parser_repl.set_defaults(func=repl)

args = parser.parse_args()
args.func(args)

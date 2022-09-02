import diff.db
import diff.config
import diff.schema
import diff.graphql
from diff.login import login
from diff.worker import Worker
from diff.storage import add_new_request
from diff.config import Config

import argparse
import coloredlogs
from logging import info

coloredlogs.install(level='DEBUG')

config: Config


def worker(args):
    worker = Worker(args.output_folder, config.gen, args.dry_run)
    worker.run()


def request(args):
    add_new_request(args.prompt, priority=10)


def migrate(args):
    diff.db.migrate(config.db)


def repl(args):
    import IPython
    IPython.embed()


def wip(args):
    w = diff.worker.SlideshowWorker()
    w.generate()


def server(args):
    import diff.server
    diff.server.run()


def export_graphql_schema(args):
    print('disabled for now')
    # diff.graphql.export()


parser = argparse.ArgumentParser(description='Generate some AI stuff')

parser.add_argument('--config',
                    help='Config file path',
                    nargs='?',
                    default='config.yaml')
parser.add_argument(
    '--dry-run',
    help='Simulate generation without actually genarting anything',
    action=argparse.BooleanOptionalAction)
parser.add_argument('--output-folder',
                    help='Prompt to use for one time generation',
                    nargs='?',
                    default='output')

subparsers = parser.add_subparsers(help='sub-command help')

parser_worker = subparsers.add_parser('worker', help='Run worker')
parser_request = subparsers.add_parser('request', help='Run prompt once')
parser_migrate = subparsers.add_parser('migrate', help='Run migrate')
parser_repl = subparsers.add_parser('repl', help='Drop into REPL')
parser_server = subparsers.add_parser('server', help='Run Flask server')
parser_export_graphql_schema = subparsers.add_parser('export-graphql-schema',
                                                     help='Run Flask server')
parser_wip = subparsers.add_parser('wip', help='Run Flask server')

parser_request.add_argument('--prompt',
                            help='Prompt to schedule a task',
                            nargs='?',
                            default='Cute cat')

parser_worker.set_defaults(func=worker)
parser_request.set_defaults(func=request)
parser_migrate.set_defaults(func=migrate)
parser_repl.set_defaults(func=repl)
parser_server.set_defaults(func=server)
parser_export_graphql_schema.set_defaults(func=export_graphql_schema)
parser_wip.set_defaults(func=wip)

args = parser.parse_args()

info(args)
config = diff.config.read(args.config)
info(config)
diff.storage.init_db_session(config.db)
login(config.hf.token)

args.func(args)

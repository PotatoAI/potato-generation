import diff.db
import diff.schema
import diff.graphql
from diff.login import login
from diff.worker import Worker
from diff.config import config

import argparse
import coloredlogs
import asyncio
from logging import info, debug

coloredlogs.install(level='INFO')


def worker(args):
    worker = Worker(
        output_dir=args.output_folder,
        gen_config=config().gen,
        nats_config=config().nats,
        video_config=config().video,
        dry_run=args.dry_run,
        until_done=args.until_done,
        task_kind=args.task_kind,
    )
    worker.run()


def migrate(args):
    diff.db.migrate(config().db)


def repl(args):
    import IPython
    IPython.embed()


def wip(args):
    w = diff.worker.SlideshowWorker(config())
    w.generate()


def server(args):
    import diff.server
    diff.server.run()


def export_graphql_schema(args):
    print('disabled for now')
    # diff.graphql.export()


parser = argparse.ArgumentParser(description='Generate some AI stuff')

parser.add_argument(
    '--config',
    help='Config file path',
    nargs='?',
    default='config.yaml',
)
parser.add_argument(
    '--verbose',
    help='Verbose output',
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    '--dry-run',
    help='Simulate generation without actually genarting anything',
    action=argparse.BooleanOptionalAction)

subparsers = parser.add_subparsers(help='sub-command help')

parser_worker = subparsers.add_parser('worker', help='Run worker')
parser_migrate = subparsers.add_parser('migrate', help='Run migrate')
parser_repl = subparsers.add_parser('repl', help='Drop into REPL')
parser_server = subparsers.add_parser('server', help='Run Flask server')
parser_export_graphql_schema = subparsers.add_parser('export-graphql-schema',
                                                     help='Run Flask server')
parser_wip = subparsers.add_parser('wip', help='Run Flask server')

parser_worker.add_argument(
    '--until-done',
    help='Run worker until all jobs are processed, then exit',
    action=argparse.BooleanOptionalAction,
)

parser_worker.add_argument(
    '--task-kind',
    help='What kind of worker to run (diffusion, upscale)',
    default='diffusion',
)

parser_worker.add_argument(
    '--output-folder',
    help='Folder to dump results',
    default='output',
)

parser_worker.set_defaults(func=worker)
parser_migrate.set_defaults(func=migrate)
parser_repl.set_defaults(func=repl)
parser_server.set_defaults(func=server)
parser_export_graphql_schema.set_defaults(func=export_graphql_schema)
parser_wip.set_defaults(func=wip)

args = parser.parse_args()

if args.verbose:
    coloredlogs.install(level='DEBUG')

debug(args)
diff.config.init_config(args.config)
debug(config())
diff.storage.init_db_session(config().db)
login(config().hf.token)

args.func(args)

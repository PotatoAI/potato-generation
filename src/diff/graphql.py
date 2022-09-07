# flask_sqlalchemy/schema.py
import glob
import graphene
import json
import asyncio
import logging
import diff.db
import logging
import base64
from datetime import datetime
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from diff.schema import Request as RequestModel, Task as TaskModel, Image as ImageModel, Video as VideoModel
from diff.worker import SlideshowWorker
from diff.storage import add_new_request, approve_requests, delete_requests, delete_tasks, delete_images, delete_videos, schedule_request, reschedule_tasks, select_images, read_binary_file
from diff.config import config
from base64 import b64decode
from typing import List


def real_id(hx: str) -> int:
    # id is base 64 encoded string "Request:9"
    decoded = b64decode(hx).decode('ascii')
    id_str = decoded.split(':')[1]

    return int(id_str)


class Request(SQLAlchemyObjectType):
    class Meta:
        model = RequestModel
        interfaces = (relay.Node, )


class Task(SQLAlchemyObjectType):
    class Meta:
        model = TaskModel
        interfaces = (relay.Node, )


class Image(SQLAlchemyObjectType):
    class Meta:
        model = ImageModel
        interfaces = (relay.Node, )


class Video(SQLAlchemyObjectType):
    class Meta:
        model = VideoModel
        interfaces = (relay.Node, )


class LargeObject(graphene.ObjectType):
    oid = graphene.NonNull(graphene.Int)
    data = graphene.NonNull(graphene.String)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    large_objects = graphene.List(lambda: LargeObject,
                                  oids=graphene.List(
                                      graphene.NonNull(graphene.Int)))

    def resolve_large_objects(self, info, oids: List[int]):
        response = []
        for oid in oids:
            bdata = read_binary_file(oid)
            data = base64.b64encode(bdata).decode('ascii')
            response.append(LargeObject(
                oid=oid,
                data=data,
            ))

        return response

    input_files = graphene.List(graphene.String)

    def resolve_input_files(self, info):
        return glob.glob('input/**/**/*')

    all_requests = SQLAlchemyConnectionField(Request.connection)
    all_tasks = SQLAlchemyConnectionField(Task.connection)
    all_images = SQLAlchemyConnectionField(Image.connection)
    all_videos = SQLAlchemyConnectionField(Video.connection)


class CreateRequest(graphene.Mutation):
    class Arguments:
        prompt = graphene.String()
        count = graphene.Int()

    ok = graphene.Boolean()
    request = graphene.Field(lambda: Request)

    def mutate(self, info, prompt, count):
        request = add_new_request(prompt, count=count)
        ok = True
        return CreateRequest(request=request, ok=ok)


class DoAction(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.NonNull(graphene.String))
        action = graphene.NonNull(graphene.String)
        model = graphene.NonNull(graphene.String)
        metadata = graphene.List(graphene.NonNull(graphene.String))

    ok = graphene.Boolean()

    def mutate(self, info, ids, action, model, metadata):
        ok = DoAction(ok=True)

        real_ids = list(map(real_id, ids))

        logging.info(f"Running {action} action on {model} {real_ids}")

        if action == 'approve' and model == 'request':
            approve_requests(real_ids)
            return ok

        if action == 'generate-video' and model == 'request':
            worker = SlideshowWorker(config().video)
            worker.generate(real_ids)
            return ok

        if action == 'add-audio' and model == 'video':
            worker = SlideshowWorker(config().video)
            worker.add_audio(real_ids, metadata)
            return ok

        if action == 'delete':
            if model == 'request':
                delete_requests(real_ids)
                return ok
            if model == 'task':
                delete_tasks(real_ids)
                return ok
            if model == 'image':
                delete_images(real_ids)
                return ok
            if model == 'video':
                delete_videos(real_ids)
                return ok

        if action == 're-run':
            if model == 'request':
                count = 1
                if len(metadata) > 0 and metadata[0]:
                    count = int(metadata[0])
                for _ in range(count):
                    for rid in real_ids:
                        schedule_request(rid)
                return ok
            if model == 'task':
                reschedule_tasks(real_ids)
                return ok

        if action == 'select' and model == 'image':
            select_images(real_ids)
            return ok

        logging.error(f"Unknown action {action} for model {model}")
        return DoAction(ok=False)


class Mutation(graphene.ObjectType):
    create_request = CreateRequest.Field()
    do_action = DoAction.Field()


# class Subscription(graphene.ObjectType):
#     change_notification = graphene.String()
#     async def subscribe_change_notification(self, info):
#         while True:
#             d = datetime.now().isoformat()
#             yield f"requests-{d}"
#             await asyncio.sleep(1)

schema = graphene.Schema(
    query=Query,
    # subscription=Subscription,
    mutation=Mutation,
)

# def export():
#     with open('ui/src/graphql/schema.json', 'w') as f:
#         json.dump(schema.introspect(), f)
#     with open('ui/src/graphql/schema.graphql', 'w') as f:
#         f.write(str(schema))

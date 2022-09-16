# flask_sqlalchemy/schema.py
import glob
import graphene
import json
import asyncio
import logging
import diff.db
import logging
import base64
import asyncio
import nats
import uuid
from datetime import datetime
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from diff.schema import Request as RequestModel, Image as ImageModel, Video as VideoModel
from diff.messages import DiffusionTask, UpscaleTask, GenVideoTask, AddAudioTask
from diff.storage import add_new_request, approve_requests, delete_requests, delete_images, delete_videos, deselect_images, select_images, read_binary_file, get_request, schedule_task, get_images
from diff.config import config
from diff.nats import nats_connect
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
        return glob.glob('input/**/*')

    all_requests = SQLAlchemyConnectionField(Request.connection)
    all_images = SQLAlchemyConnectionField(Image.connection)
    all_videos = SQLAlchemyConnectionField(Video.connection)

    images_by_id = graphene.List(Image,
                                 image_ids=graphene.List(
                                     graphene.NonNull(graphene.String)))

    def resolve_images_by_id(self, info, image_ids) -> List[ImageModel]:
        real_ids = list(map(real_id, image_ids))
        return get_images(real_ids)


async def mutate_async(info, prompt, count) -> RequestModel:
    nc = await nats_connect(config().nats.url())
    res = await add_new_request(nc, prompt, count=count)
    await nc.flush(timeout=1)
    await nc.close()
    return res


class CreateRequest(graphene.Mutation):
    class Arguments:
        prompt = graphene.String()
        count = graphene.Int()

    ok = graphene.Boolean()
    request = graphene.Field(lambda: Request)

    def mutate(self, info, prompt, count):
        loop = asyncio.new_event_loop()
        request = loop.run_until_complete(mutate_async(info, prompt, count))
        loop.close()
        ok = True
        return CreateRequest(request=request, ok=ok)


async def do_action_async(info, ids, action, model, metadata) -> bool:
    ok = True
    nc = await nats_connect(config().nats.url())

    real_ids = list(map(real_id, ids))

    logging.info(
        f"Running {action} action on {model} {real_ids} -> {metadata}")

    if action == 'approve' and model == 'request':
        approve_requests(real_ids)
        return ok

    if action == 'generate-video' and model == 'request':
        for rid in real_ids:
            uid = str(uuid.uuid1())
            task = GenVideoTask(uid=uid, request_id=rid)
            await schedule_task(nc, task)
        return ok

    if action == 'add-audio' and model == 'video':
        for vid in real_ids:
            uid = str(uuid.uuid1())
            task = AddAudioTask(uid=uid, video_id=vid, file_path=metadata[0])
            await schedule_task(nc, task)
        return ok

    if action == 'delete':
        if model == 'request':
            delete_requests(real_ids)
            return ok
        if model == 'image':
            delete_images(real_ids)
            return ok
        if model == 'video':
            delete_videos(real_ids)
            return ok

    if action == 'copy' and model == 'request':
        for rid in real_ids:
            request = get_request(rid)
            count = 5
            if len(metadata) > 0 and metadata[0]:
                count = int(metadata[0])
            await add_new_request(nc, request.prompt, count=count)

    if action == 'upscale' and model == 'request':
        for rid in real_ids:
            request = get_request(rid)
            for img in request.images:
                uid = str(uuid.uuid1())
                task = UpscaleTask(uid=uid, image_id=img.id)
                await schedule_task(nc, task)
        return ok

    if action == 're-run':
        if model == 'request':
            count = 1
            if len(metadata) > 0 and metadata[0]:
                count = int(metadata[0])
            for _ in range(count):
                for rid in real_ids:
                    uid = str(uuid.uuid1())
                    task = DiffusionTask(uid=uid, request_id=rid)
                    await schedule_task(nc, task)
            return ok

    if action == 'select' and model == 'image':
        select_images(real_ids)
        return ok

    if action == 'deselect' and model == 'image':
        deselect_images(real_ids)
        return ok

    logging.error(f"Unknown action {action} for model {model}")
    await nc.flush(timeout=1)
    await nc.close()
    return False


class DoAction(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.NonNull(graphene.String))
        action = graphene.NonNull(graphene.String)
        model = graphene.NonNull(graphene.String)
        metadata = graphene.List(graphene.NonNull(graphene.String))

    ok = graphene.Boolean()

    def mutate(self, info, ids, action, model, metadata):
        loop = asyncio.new_event_loop()
        ok = loop.run_until_complete(
            do_action_async(info, ids, action, model, metadata))
        loop.close()
        return DoAction(ok=ok)


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

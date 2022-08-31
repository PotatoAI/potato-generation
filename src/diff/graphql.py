# flask_sqlalchemy/schema.py
import graphene
import json
import asyncio
import logging
import diff.db
from datetime import datetime
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from diff.schema import Request as RequestModel, Task as TaskModel, Image as ImageModel
from diff.storage import add_new_request, approve_request
from base64 import b64decode


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


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_requests = SQLAlchemyConnectionField(Request.connection)
    all_tasks = SQLAlchemyConnectionField(Task.connection)
    all_images = SQLAlchemyConnectionField(Image.connection)


class CreateRequest(graphene.Mutation):
    class Arguments:
        prompt = graphene.String()

    ok = graphene.Boolean()
    request = graphene.Field(lambda: Request)

    def mutate(root, info, prompt):
        request = add_new_request(prompt)
        ok = True
        return CreateRequest(request=request, ok=ok)


class ApproveRequest(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()

    def mutate(root, info, id):
        approve_request(real_id(id))
        ok = True
        return ApproveRequest(ok=ok)


class Mutation(graphene.ObjectType):
    create_request = CreateRequest.Field()
    approve_request = ApproveRequest.Field()


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

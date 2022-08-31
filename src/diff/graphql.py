# flask_sqlalchemy/schema.py
import graphene
import json
import asyncio
from datetime import datetime
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .schema import Request as RequestModel, Task as TaskModel, Image as ImageModel


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


class Subscription(graphene.ObjectType):
    change_notification = graphene.String()

    async def subscribe_change_notification(self, info):
        while True:
            d = datetime.now().isoformat()
            yield f"requests-{d}"
            await asyncio.sleep(1)


schema = graphene.Schema(query=Query, subscription=Subscription)


def export():
    with open('ui/src/graphql/schema.json', 'w') as f:
        json.dump(schema.introspect(), f)
    # with open('ui/src/graphql/schema.graphql', 'w') as f:
    #     f.write(str(schema))

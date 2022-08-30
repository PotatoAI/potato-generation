# flask_sqlalchemy/schema.py
import graphene
import json
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
    # Disable sorting over this field
    # all_departments = SQLAlchemyConnectionField(Department.connection, sort=None)


schema = graphene.Schema(query=Query)


def export():
    with open('codegen/schema.json', 'w') as fp:
        json.dump(schema.introspect(), fp)

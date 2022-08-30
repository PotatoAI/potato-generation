from flask import Flask
from flask_graphql import GraphQLView

from .graphql import schema

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    ),
)


def run(sess):
    app.run()
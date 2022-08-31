from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from diff.graphql import schema

app = Flask(__name__)
CORS(app)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    ),
)


def run():
    app.run()

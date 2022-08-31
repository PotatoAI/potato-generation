from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from .graphql import schema

app = Flask(__name__)
CORS(app)
app.debug = True
db_session = None

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    ),
)


def run(sess):
    global db_session
    db_session = sess
    app.run()

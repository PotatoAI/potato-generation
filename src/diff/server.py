from flask import Flask, Response
from flask_graphql import GraphQLView
from flask_cors import CORS
from diff.graphql import schema, real_id
from diff.storage import get_image_data, get_video_data

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

def try_parse_int(s: str) -> int:
    if s.isdigit():
        return int(s)
    else:
        return real_id(s)

@app.route("/image/<id>")
def image(id):
    data = get_image_data(try_parse_int(id))
    resp = Response(data)
    resp.headers['Content-Type'] = 'image/png'
    return resp

@app.route("/video/<id>")
def video(id):
    data = get_video_data(try_parse_int(id))
    resp = Response(data)
    resp.headers['Content-Type'] = 'video/mp4'
    return resp


def run():
    app.run()

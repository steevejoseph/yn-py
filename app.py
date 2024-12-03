from flask import Flask, send_from_directory
import os
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

from utils import MyClassJSONEncoder

from ynt.chats.views import chat_router
from ynt.users.views import user_router
from ynt.index.views import index_router


app = Flask(__name__, static_folder="static/dist", static_url_path="")
# app.json_encoder_class = MyClassJSONEncoder
app.json_encoder = MyClassJSONEncoder
CORS(app)

PORT = os.environ.get("PORT") or "8080"
DEBUG = os.environ.get("FLASK_DEBUG") or False


@app.route("/", defaults={"path": ""})
def serve(path):
    return send_from_directory(app.static_folder, "index.html")


app.register_blueprint(index_router, url_prefix="/api")
app.register_blueprint(user_router, url_prefix="/api/users")
app.register_blueprint(chat_router, url_prefix="/api/chats")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

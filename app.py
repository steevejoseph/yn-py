from flask import Flask
import os
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

from utils import MyClassJSONEncoder

from ynt.chats.views import chat_router
from ynt.users.views import user_router
from ynt.index.views import index_router


app = Flask(__name__)
# app.json_encoder_class = MyClassJSONEncoder
app.json_encoder = MyClassJSONEncoder
CORS(app)

PORT = os.environ.get("PORT") or "8080"
DEBUG = os.environ.get("FLASK_DEBUG") or False

app.register_blueprint(index_router)
app.register_blueprint(user_router)
app.register_blueprint(chat_router)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

import json
from flask import Flask, request, Response, render_template, jsonify
from openai import OpenAI, ChatCompletion
import os
from flask_cors import CORS
import mongoengine

from dotenv import load_dotenv
from mongodb import add_chat, add_user, get_chats_for_user, get_user_by_id
from type_definitions import User
from utils import MyClassJSONEncoder, create_chat_completion, create_response


load_dotenv()


app = Flask(__name__)
app.json_encoder = MyClassJSONEncoder
CORS(app)


@app.route('/', methods=["GET"])
def handle_home() -> Response:
    return render_template("index.html")


@app.route('/chat', methods=['POST'])
def handle_chat() -> Response:
    try:
        data = request.get_json()
    except:
        return create_response("Please submit valid JSON", 400)

    content = data.get("content")
    role = data.get("role") or "helpful assistant"

    if content == None:
        return create_response("Please specify 'content' in your json", 400)

    completion = create_chat_completion(content, role)
    # print(f"completion: {completion}")
    completion = add_chat(completion, None)

    return create_response("Successfully created chat", 200, data={"chat": completion})


@app.route("/user", methods=["POST"])
def handle_add_user() -> Response:
    data = request.get_json()
    user_dict = data.get("user")
    user = User(**user_dict)

    try:
        new_user = add_user(user)
        return create_response("user added successfully", 200, {"user": new_user})
    except mongoengine.ValidationError as ve:
        return create_response(
            "Bad request, please include valid input",
            400,
            reason=str(ve),
            data={"user": user},
        )
    except Exception as e:
        return create_response(
            "failed to add user :\(", 500, reason=str(e), data={"user": user}
        )


@app.route("/users/<id>/chats", methods=["GET"])
def handle_get_user_chats(id):

    if not id:
        return create_response("Please specify a user ID", 400)

    userModel = get_user_by_id(id)

    if not userModel:
        return create_response(f"No user found for id [{id}]", 404)

    chatModels = get_chats_for_user(id)

    if not chatModels or len(chatModels) == 0:
        return create_response(f"No chats for user with email [{userModel.email}]", 404)

    return create_response(
        "Successfully fetched chats for user", 200, data={"chats": chatModels}
    )


@app.route("/users/<id>", methods=["GET"])
def handle_get_user_by_id(id):
    if not id:
        return create_response("Please specify a user ID", 400)

    userModel = get_user_by_id(id)

    if not userModel:
        return create_response(f"No user found for id [{id}]", 404)
    return create_response(f"Successfully fetched user", 200, data={"user": userModel})


PORT = os.environ.get("PORT") or "8080"
DEBUG = os.environ.get("FLASK_DEBUG") or False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

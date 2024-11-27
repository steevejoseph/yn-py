from flask import Blueprint, Response, request

from utils import create_response
from ynt.chats.controllers import add_chat
from ynt.chats.utils import create_chat_completion

chat_router = Blueprint("chat_router", __name__, template_folder="templates")


@chat_router.route("/chat", methods=["POST"])
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

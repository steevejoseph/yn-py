from flask import Blueprint, Response, request
import mongoengine

from type_definitions import User
from utils import create_response
from ynt.users.controllers import add_user, get_chats_for_user, get_user_by_id


user_router = Blueprint("user_router", __name__, template_folder="templates")


@user_router.route("/user", methods=["POST"])
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


@user_router.route("/users/<id>/chats", methods=["GET"])
def handle_get_user_chats(id):

    if not id:
        return create_response("Please specify a user ID", 400)

    userModel = get_user_by_id(id)

    if not userModel:
        return create_response(f"No user found for id [{id}]", 404)

    chatModels = get_chats_for_user(id)

    if chatModels == None:
        return create_response(f"No chats for user with email [{userModel.email}]", 404)

    return create_response(
        "Successfully fetched chats for user", 200, data={"chats": chatModels}
    )


@user_router.route("/users/<id>", methods=["GET"])
def handle_get_user_by_id(id):
    if not id:
        return create_response("Please specify a user ID", 400)

    userModel = get_user_by_id(id)

    if not userModel:
        return create_response(f"No user found for id [{id}]", 404)
    return create_response(f"Successfully fetched user", 200, data={"user": userModel})

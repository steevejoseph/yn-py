from flask import Blueprint, Response, render_template, request
import mongoengine
from mongodb import add_user, get_chats_for_user, get_user_by_id
from type_definitions import User
from utils import create_response


index_router = Blueprint("index_router", __name__, template_folder="templates")


@index_router.route("/", methods=["GET"])
# @app.route("/", methods=["GET"])
def handle_home() -> Response:
    return render_template("index.html")

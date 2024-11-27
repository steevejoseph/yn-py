from flask import Blueprint, Response, render_template, request


index_router = Blueprint("index_router", __name__, template_folder="templates")


@index_router.route("/", methods=["GET"])
# @app.route("/", methods=["GET"])
def handle_home() -> Response:
    return render_template("index.html")

from flask import (
    Blueprint,
    Response,
    json,
    send_from_directory,
)


index_router = Blueprint("index_router", __name__, template_folder="templates")


@index_router.route("/", methods=["GET"])
def handle_home() -> Response:
    return send_from_directory(directory="static/dist", path="index.html")


@index_router.route("/ping", methods=["GET"])
def handle_ping():
    print("Ping route hit")
    return Response(
        json.dumps({"message": "pong"}), status=200, mimetype="application/json"
    )

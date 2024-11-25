from flask import Flask, request, Response, render_template, jsonify
from openai import OpenAI
import os
from flask_cors import CORS

from dotenv import load_dotenv

from firestore import add_user

load_dotenv()

app = Flask(__name__)
api_key = os.environ["YN_KEY"]
client = OpenAI(api_key=api_key)
CORS(app)


def create_response(message: str, status_code: int, data=None) -> Response:
    res = jsonify({"message": message, "data": data})
    res.status_code = status_code
    return res


@app.route('/', methods=["GET"])
def handle_home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
    except:
        return create_response("Please submit valid JSON", 400)

    print("data:", data)

    content = data.get("content")
    role = data.get("role") or "helpful assistant"

    if content == None:
        return create_response("Please specify 'content' in your json", 400)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Speak as if you were a {role}."},
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=100
    )

    responseMessage = completion.choices[0].message.content
    return create_response(responseMessage, 200)


@app.route("/user", methods=["POST"])
def handle_add_user():
    data = request.get_json()
    user = data.get("user")

    try:
        new_user = add_user(user)
        return create_response("user added successfully", 200, {"user": new_user})
    except Exception as e:
        return create_response("failed to add user :\(", 500, {"reason": e})


PORT = os.environ.get("PORT") or "8080"
DEBUG = os.environ.get("FLASK_DEBUG") or False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

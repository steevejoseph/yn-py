from flask import Flask, request, Response, render_template
from openai import OpenAI
import os
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
api_key = os.environ["YN_KEY"]
client = OpenAI(api_key=api_key)
CORS(app)

class ResponseMessage:
    def __init__(self, status, message) -> None:
        self.status = status
        self.message = message
        return
    
@app.route('/', methods=["GET"])
def handle_home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
    except:
        return Response("Please submit valid JSON", 400, mimetype="application/json")
        
    print("data:", data)

    content = data.get("content")
    role = data.get("role") or "helpful assistant"
    language = data.get("language") or data.get("lang") or "english"
    
    if content == None:
        return  Response("Please specify 'content' in your json", status=400, mimetype="application/json")
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Speak as if you were a {role}."},
            {"role": "system", "content": f"Return in the {language} language."},
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=100
    )
        
    responseMessage = completion.choices[0].message.content
    return Response({"message": responseMessage}, 200, mimetype="application/json")

PORT = os.environ.get("PORT") or "8080"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
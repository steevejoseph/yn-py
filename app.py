from flask import Flask, request, Response
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)
api_key = os.environ["YN_KEY"]
client = OpenAI(api_key=api_key)

class ResponseMessage:
    def __init__(self, status, message) -> None:
        self.status = status
        self.message = message
        return
    
@app.route('/', methods=["GET"])
def handle_home():
    return Response(None, 200)

@app.route('/chat', methods=['POST'])
def handle_chat():
    print("d:", request.data)
    
    try:
        data = request.get_json()
    except:
        return Response("Please submit valid JSON", 400, mimetype="application/json")
        
    print("data:", data)

    content = data.get("content")
    role = data.get("role") or "helpful assistant"
    
    if content == None:
        return  Response("Please specify 'content' in your json", status=400, mimetype="application/json")
    
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
    return Response(responseMessage, 200, mimetype="application/json")
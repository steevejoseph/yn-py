import json
import os
from flask import Response, jsonify
from openai import OpenAI, ChatCompletion
from dotenv import load_dotenv

load_dotenv()


def create_response(message: str, status_code: int, data=None, reason=None) -> Response:
    res = jsonify({"message": message, "data": data, "reason": reason})
    res.status_code = status_code
    return res


open_ai_api_key = os.environ["YN_KEY"]
open_ai_client = OpenAI(api_key=open_ai_api_key)


def create_chat_completion(content: str, role: str) -> ChatCompletion:
    return open_ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Speak as if you were a {role}."},
            {"role": "user", "content": content},
        ],
        max_tokens=100,
    )


class MyClassJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, object):
            return obj.to_dict()  # Serialize MyClass instances using to_dict
        return super().default(obj)  # Let the default encoder handle other types

from openai import OpenAI, ChatCompletion
import os

from dotenv import load_dotenv

load_dotenv()


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

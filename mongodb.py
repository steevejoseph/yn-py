import logging
from pymongo import MongoClient
import os
import mongoengine
from type_definitions import ChatCompletion
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

from models import UserModel, ChatModel

uri = os.environ.get("MONGO_DB_CONNECTION_STRING")
db_name = os.environ.get("MONGO_DB_DB_NAME")

if not uri:
    raise Exception("No connection string found in environment variables :(")
if not db_name:
    raise Exception("No database name found in environment variables :(")

mongoengine.connect(host=uri, db=db_name)


def add_user(user: UserModel) -> UserModel:
    userModel = UserModel(
        name=user.name,
        email=user.email,
        password=user.password,
    )

    try:
        userModel.save()
        user.id = str(userModel.id)
        # print(userModel)
        return user
    except mongoengine.ValidationError as ve:
        logging.error(f"Failed to validate user {str(ve)}")
        print(ve)
        raise ve


def add_chat(completion: ChatCompletion) -> ChatCompletion:
    timestamp_millis = completion.created
    created_at = datetime.fromtimestamp(timestamp_millis / 1000)
    # print(f"UNIX epoch time: {timestamp_millis}")
    chatModel = ChatModel(
        created_at=created_at,
        model=completion.model,
        content=completion.choices[0].message.content,
    )

    try:
        chatModel.save()
        completion.id = str(chatModel.id)
        completion.content = chatModel.content
        # print(completion)
        return completion
    except mongoengine.ValidationError as ve:
        logging.error(f"Failed to validate chat {str(ve)}")
        print(ve)
        raise ve

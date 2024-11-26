import logging
from typing import List
from pymongo import MongoClient
import os
import mongoengine
from bson import ObjectId
from type_definitions import ChatCompletion, User
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


def add_user(user: User) -> UserModel:
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


def add_chat(completion: ChatCompletion, user: User = None) -> ChatCompletion:
    chatModel = ChatModel(
        model=completion.model,
        content=completion.choices[0].message.content,
    )

    if user != None:
        associate_chat_with_user(user, chatModel)
        chatModel.user_ref = ObjectId(user.id)

    try:
        chatModel.save()
        completion.id = str(chatModel.id)
        completion.content = chatModel.content
        return completion
    except mongoengine.ValidationError as ve:
        logging.error(f"Failed to validate chat {str(ve)}")
        print(ve)
        raise ve


def associate_chat_with_user(user: User, chatModel: ChatModel):
    # print("Current user:", user)
    user_id = ObjectId(user.id)
    matches = UserModel.objects(id=user_id)
    matching_user: UserModel = matches[0]
    object_id = ObjectId(chatModel.id)
    matching_user.chats.append(object_id)
    matching_user.save()


def get_chats_for_user(user_id: str) -> List[ChatModel]:
    id = ObjectId(user_id.strip())
    matching_user: UserModel = UserModel.objects(id=id).first()

    user_chats = ChatModel.objects(user_ref=matching_user.id)
    print("matching chats:", user_chats)
    return [chatModel.to_chatcompletion() for chatModel in user_chats]


def get_user_by_id(user_id: str) -> User:
    id = ObjectId(user_id.strip())
    matching_users: List[UserModel] = list(UserModel.objects(id=id))

    user_model = None if len(matching_users) < 1 else matching_users[0]

    if not user_model:
        return None

    return user_model.to_user()

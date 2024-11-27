import logging
from typing import List
import mongoengine
from bson import ObjectId
from type_definitions import User

from dotenv import load_dotenv

from ynt.chats.models import ChatModel
from ynt.users.models import UserModel
from mongodb import connection

load_dotenv()


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


def get_user_by_id(user_id: str) -> User:
    id = ObjectId(user_id.strip())
    matching_users: List[UserModel] = list(UserModel.objects(id=id))

    user_model = None if len(matching_users) < 1 else matching_users[0]

    if not user_model:
        return None

    return user_model.to_user()


def get_chats_for_user(user_id: str) -> List[ChatModel]:
    id = ObjectId(user_id.strip())
    matching_user: UserModel = UserModel.objects(id=id).first()

    user_chats = ChatModel.objects(user_ref=matching_user.id)
    print("matching chats:", user_chats)
    return [chatModel.to_chatcompletion() for chatModel in user_chats]

import logging
import mongoengine
from bson import ObjectId
from type_definitions import ChatCompletion, User

from dotenv import load_dotenv

from ynt.chats.models import ChatModel
from ynt.users.models import UserModel
from mongodb import connection

load_dotenv()


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

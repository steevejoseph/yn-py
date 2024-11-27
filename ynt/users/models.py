from bson import ObjectId
from mongoengine import *

from type_definitions import User
from ynt.chats.models import ChatModel
from ynt.index.models import BaseDocument


class UserModel(BaseDocument):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    chats = ListField(ReferenceField(ChatModel), required=False, default=[])

    meta = {"collection": f"users_collection"}

    def to_dict(self):
        """
        Converts the document's fields to a dictionary.
        """

        return {
            field: (
                str(getattr(self, field))
                if isinstance(getattr(self, field), ObjectId)
                else getattr(self, field)
            )
            for field in self._fields
        }

    def to_user(self) -> User:
        """
        Converts this UserModel instance to a User instance.

        Returns:
            User: A new User instance with data from this UserModel.
        """
        user_data = self.to_dict()
        # Map the fields as necessary (e.g., rename "_id" to "id")
        user_data["id"] = str(user_data.pop("_id", None))
        user_data["chats"] = [str(chat.id) for chat in self.chats]
        return User(**user_data)

from bson import ObjectId
from mongoengine import *
from pprint import pformat
import datetime

from type_definitions import ChatCompletion, User
from ynt.index.models import BaseDocument


class ChatModel(BaseDocument):

    # We need to figure out how to generate this
    link = StringField(required=False)

    created_at = DateTimeField(
        required=True, default=datetime.datetime.now(datetime.timezone.utc)
    )
    content = StringField(required=True)
    model = StringField()
    user_ref = ReferenceField("UserModel")

    meta = {"collection": f"chats_collection"}

    def to_dict(self):
        """
        Converts the document's fields to a dictionary using dictionary comprehension.
        Handles ObjectId by converting it to a string.
        """
        return {
            field: (
                str(getattr(self, field))
                if isinstance(getattr(self, field), ObjectId)
                else getattr(self, field)
            )
            for field in self._fields
        }

    def to_chatcompletion(self):
        """
        Converts the ChatModel instance to a ChatCompletion instance.
        """
        # Extract fields from the ChatModel instance
        return ChatCompletion(
            content=self.content,
            created_at=self.created_at,
            model=self.model,
            id=str(self.id),  # Convert the ObjectId to a string
        )

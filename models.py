from mongoengine import *
from pprint import pformat


class BaseDocument(Document):
    meta = {"abstract": True}
    collection_prefix = StringField(required=True)

    def __str__(self):
        fields = {field: getattr(self, field) for field in self._fields}
        return f"{self.__class__.__name__}({pformat(fields)})"

    def save(self, *args, **kwargs):
        self._meta["collection"] = f"{self.collection_prefix}_collection"
        super().save(*args, **kwargs)


class ChatModel(BaseDocument):
    collection_prefix = StringField(required=True, default="chats")

    # We need to figure out how to generate this
    link = StringField(required=False)

    created_at = DateTimeField(required=True)
    content = StringField(required=True)
    model = StringField()


class UserModel(BaseDocument):
    collection_prefix = StringField(required=True, default="users")
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    chats = ListField(ReferenceField(ChatModel), required=False, default=[])

from mongoengine import Document, StringField


class User(Document):
    name = StringField(required=True)
    booba = StringField(required=False)

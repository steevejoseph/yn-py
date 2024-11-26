import logging
from pymongo import MongoClient
import os
import mongoengine

from dotenv import load_dotenv

load_dotenv()

from models import User

uri = os.environ.get("MONGO_DB_CONNECTION_STRING")

if not uri:
    raise Exception("No connection string found in environment variables :(")

mongoengine.connect(host=uri)


def add_user(user: dict):
    userModel = User(name=user.get("name"))
    try:
        document = userModel.save()
        user["_id"] = str(document.id)
        print(userModel.id)
        return user
    except mongoengine.ValidationError as ve:
        logging.error(f"Failed to validate user {str(ve)}")
        print(ve)
        raise ve

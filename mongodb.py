from pymongo import MongoClient
import os
import mongoengine

from dotenv import load_dotenv

load_dotenv()

uri = os.environ.get("MONGO_DB_CONNECTION_STRING")
db_name = os.environ.get("MONGO_DB_DB_NAME")

if not uri:
    raise Exception("No connection string found in environment variables :(")
if not db_name:
    raise Exception("No database name found in environment variables :(")

connection = mongoengine.connect(host=uri, db=db_name, alias="default")


def remove_field_from_documents(uri: str, collection_name: str, field: str):
    mongoengine.disconnect()

    # Connect to MongoDB
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    # Remove the field from documents where it exists
    result = collection.update_many(
        {field: {"$exists": True}},  # Match documents where the field exists
        {"$unset": {"collection_prefix": ""}},  # Remove the field
    )

    print(f"Removed field from {result.modified_count} documents")
    client.close()
    mongoengine.connect(host=uri, db=db_name)

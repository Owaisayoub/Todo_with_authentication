from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os

uri = os.getenv("DATABASE_URL")


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo_db

#create a collection inside our db and name that as todo_collection
todo_collection = db["todo_collection"]
user_collection = db["user_collection"]
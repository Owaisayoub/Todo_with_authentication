from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://oemollic:mqldsqsDTRZ24xd4@cluster5.htqtvib.mongodb.net/?retryWrites=true&w=majority&appName=Cluster5"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo_db

#create a collection inside our db and name that as todo_collection
todo_collection = db["todo_collection"]
user_collection = db["user_collection"]
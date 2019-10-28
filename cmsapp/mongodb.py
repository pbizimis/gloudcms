from pymongo import MongoClient
from pprint import pprint

DATABASE_URI = 'mongodb://localhost:27017/'

client = MongoClient(DATABASE_URI)
dbtest = client.glouddb.list_collection_names()
db = client.glouddb
#test_user = db.user.insert_one({"user-id": "0001"})
pprint(db.user.find_one())

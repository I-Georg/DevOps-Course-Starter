import pymongo
from  datetime import datetime
from bson import ObjectId

id = "612dfa5e366842b65f9c9d33"
client = pymongo.MongoClient(
    "mongodb+srv://admin:MongoAdmin1@cluster0.qtpde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
database = client["01"]
post = {"_id": ObjectId(id)}
trello_collection = database["trello_collection"]
dateNow = datetime.now()
result = trello_collection.update_one(
    post, {"$set": {"idBoard": "not really a a board id", "last_modified": dateNow}}
)
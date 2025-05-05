from pymongo import MongoClient
import os 

mongo_uri = os.getenv("mongodb_uri") if os.getenv("mongodb_uri") else "mongodb://admin:password123@localhost:27017/"
client = MongoClient(mongo_uri)
db = client.trends_db
collection = db.trends

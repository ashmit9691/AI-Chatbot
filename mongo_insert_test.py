from pymongo import MongoClient
import datetime
import uuid

client = MongoClient("mongodb://localhost:27017/")
db = client["chatbotDB"]
collection = db["chatHistory"]

session_id = str(uuid.uuid4())

collection.insert_one({
    "session_id": session_id,
    "role": "user",
    "message": "Testing direct insert!",
    "timestamp": datetime.datetime.utcnow()
})

print(f" Test message inserted with session_id: {session_id}")

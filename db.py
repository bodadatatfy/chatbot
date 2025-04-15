from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "chatbot")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "conversations")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_chat_to_db(user_input, bot_response, tag):
    """Save conversation to MongoDB"""
    try:
        collection.insert_one({
            "user_input": user_input,
            "bot_response": bot_response,
            "tag": tag,
            "timestamp": datetime.utcnow()
        })
    except Exception as e:
        print(f"Error saving to database: {e}")
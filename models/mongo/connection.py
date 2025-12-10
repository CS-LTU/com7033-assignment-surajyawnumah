from config import Config
from pymongo import MongoClient

def mongo_conn():
    """Establish MongoDB connection"""
    try:
        client = MongoClient(Config.MONGO_URI)
        mdb = client[Config.MONGO_DB]
        return client, mdb
    except Exception as e:
        print(f"MongoDB connection error: {str(e)}")
        return None, None
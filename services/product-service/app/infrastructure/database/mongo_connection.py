from pymongo import MongoClient
import os

def get_database():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI não definida")

    client = MongoClient(mongo_uri)
    return client["product_db"]
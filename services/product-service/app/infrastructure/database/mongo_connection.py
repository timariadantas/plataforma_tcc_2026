import os
from pymongo import MongoClient
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

_client = None

def get_database():
    global _client

    if _client is None:
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            logger.error("MONGO_URI não definida")
            raise ValueError("MONGO_URI não definida")

        logger.info("Conectando ao MongoDB...")
        _client = MongoClient(mongo_uri)

    return _client["product_db"]
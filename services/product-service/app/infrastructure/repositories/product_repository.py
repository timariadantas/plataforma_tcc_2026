from pymongo import MongoClient
from infrastructure.logging.logger import logger
from infrastructure.database.mongo_connection import get_database




class ProductRepository:

    def __init__(self):
      db = get_database()
      self.collection = db["products"]

    def save(self, product):    
        try:                                                                  
            logger.info("Saving product")
            data = product.to_dict()
            data["_id"] = data["id"]      ## Mongo precisa disso
            self.collection.insert_one(data)
        except Exception as e:
            logger.error(f"Error saving product: {e}")
            raise

    def get_all(self, page=1, limit=10):
        try:
            logger.info(f"Fetching produts page={page} limit={limit}")
            skip = (page - 1) * limit
            return list(
                self.collection.find({"active": True})
                .skip(skip)
                .limit(limit)
                )
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            raise ValueError("DataBase Error") from e
          

    def get_by_id(self, product_id):
        logger.info("searching for product by ID")
        product = self.collection.find_one({
            "_id": product_id,
            "active": True
        })

        if not product:
            logger.warning(f"Product not found: {product_id}")
            raise ValueError("Product not found")

        return product
    def update(self, product_id, data):
        result = self.collection.update_one(
            {"_id": product_id},
            {"$set": data}
        )
        if result.matched_count == 0:
            logger.warning(f"Update failed, product not found: {product_id}")
            raise ValueError("Product not found")

    def delete(self, product_id):
        result = self.collection.update_one(
            {"_id": product_id},
            {"$set": {"active": False}}
        )
        if result.matched_count == 0:
            logger.warning(f"Delete failed, product not found: {product_id}")
            raise ValueError("Product not found")
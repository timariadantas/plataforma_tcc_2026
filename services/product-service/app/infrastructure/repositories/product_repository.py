from pymongo import MongoClient

class ProductRepository:

    def __init__(self):
        client = MongoClient("mongodb://localhost:27017")
        db = client["product_db"]
        self.collection = db["products"]

    def save(self, product):
        self.collection.insert_one(product.to_dict())

    def get_all(self):
        return list(self.collection.find({"active": True}))

    def get_by_id(self, product_id):
        return self.collection.find_one({"_id": product_id, "active": True})

    def update(self, product_id, data):
        self.collection.update_one(
            {"_id": product_id},
            {"$set": data}
        )

    def delete(self, product_id):
        self.collection.update_one(
            {"_id": product_id},
            {"$set": {"active": False}}
        )
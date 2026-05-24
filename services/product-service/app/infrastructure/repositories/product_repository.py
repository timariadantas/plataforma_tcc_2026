from datetime import datetime, timezone
from app.infrastructure.database.mongo_connection import get_database
from app.infrastructure.logging.logger import get_logger
from app.domain.entities.product import Product

logger = get_logger(__name__)


class ProductRepository:

    def __init__(self, db= None):
        if db is None:
            db = get_database()
        self.collection = db["products"]

    def save(self, product: Product):
        try:
            logger.info(f"Saving product: {product.id}")

            data = {
                "_id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "quantity": product.quantity,
                "created_at": product.created_at,
                "updated_at": product.updated_at,
                "active": product.active
            }

            self.collection.insert_one(data)

            logger.info("Product saved successfully")

        except Exception as e:
            logger.error(f"Error saving product: {e}")
            raise

    def find_by_id(self, product_id: str) -> Product:
        try:
            logger.info(f"Finding product: {product_id}")

            doc = self.collection.find_one({"_id": product_id})

            if not doc:
                logger.warning(f"Product not found: {product_id}")
                raise ValueError("Product not found")

            return Product(
                id=str(doc["_id"]),
                name=doc["name"],
                description=doc.get("description"),
                price=doc["price"],
                quantity=doc["quantity"],
                created_at=doc.get("created_at"),
                updated_at=doc.get("updated_at"),
                active=doc.get("active", True)
            )

        except Exception as e:
            logger.error(f"Error finding product: {e}")
            raise

    def find_all(self, page=1, limit=10):
        try:
            logger.info(f"Fetching products page={page}, limit={limit}")

            skip = (page - 1) * limit

            docs = list(
                self.collection.find()
                .skip(skip)
                .limit(limit)
            )

            logger.info(f"Total products fetched: {len(docs)}")

            return [
                Product(
                    id=str(d["_id"]),
                    name=d["name"],
                    description=d.get("description"),
                    price=d["price"],
                    quantity=d["quantity"],
                    created_at=d.get("created_at"),
                    updated_at=d.get("updated_at"),
                    active=d.get("active", True)
                )
                for d in docs
            ]

        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            raise

    def update(self, product_id: str, data: dict):
        try:
            logger.info(f"Updating product: {product_id}")

            data["updated_at"] = datetime.now(timezone.utc)

            result = self.collection.update_one(
                {"_id": product_id},
                {"$set": data}
            )

            if result.matched_count == 0:
                logger.warning(f"Product not found for update: {product_id}")
                raise ValueError("Product not found")

            logger.info("Product updated successfully")

        except Exception as e:
            logger.error(f"Error updating product: {e}")
            raise

    def delete(self, product_id: str):
        try:
            logger.info(f"Deleting product: {product_id}")

            result = self.collection.update_one(
                {"_id": product_id},
                {
                    "$set": {
                        "active": False,
                        "updated_at": datetime.now(timezone.utc)
                    }
                }
            )

            if result.matched_count == 0:
                logger.warning(f"Product not found for delete: {product_id}")
                raise ValueError("Product not found")

            logger.info("Product deleted successfully")

        except Exception as e:
            logger.error(f"Error deleting product: {e}")
            raise

    def decrease_stock(self, product_id: str, quantity: int):
        try:
            logger.info(f"Decreasing stock: {product_id}")

            doc = self.collection.find_one({"_id": product_id})

            if not doc:
                raise ValueError("Product not found")

            if doc["quantity"] < quantity:
                raise ValueError("Insufficient stock")

            self.collection.update_one(
                {"_id": product_id},
                {
                    "$inc": {"quantity": -quantity},
                    "$set": {"updated_at": datetime.now(timezone.utc)}
                }
            )

            logger.info("Stock updated successfully")

        except Exception as e:
            logger.error(f"Error decreasing stock: {e}")
            raise
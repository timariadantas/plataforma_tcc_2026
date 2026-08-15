from datetime import datetime, timezone
from infrastructure.database.mongo_connection import get_database
from infrastructure.logging.logger import get_logger
from domain.entities.product import Product
from domain.repositories.product_repository_interface import ProductRepositoryInterface
from application.mapper.product_mapper import ProductMapper
from infrastructure.errors.service_errors import( 
ProductNotFoundError,
InsufficientStockError ,
ServiceError,
DatabaseUnavailableError)

logger = get_logger(__name__)

class ProductRepository(ProductRepositoryInterface):

    def __init__(self, db= None):
        if db is None:
            db = get_database()
        self.collection = db["products"]

    def save(self, product: Product):
        try:
            logger.info(f"Saving product: {product.id}")

            data = ProductMapper.to_document(product)

            self.collection.insert_one(data)

            logger.info("Product saved successfully")

        except ServiceError:
            raise

        except Exception as e:
            logger.error(f"Database error while saving product: {e}")
            raise DatabaseUnavailableError("Database unavailable") from e

    def find_by_id(self, product_id: str) -> Product:
        try:
            logger.info(f"Finding product: {product_id}")

            doc = self.collection.find_one({"_id": product_id})

            if not doc:
                logger.warning(f"Product not found: {product_id}")
                raise ProductNotFoundError("Product not found")

            return  ProductMapper.from_document(doc)
        
        except ServiceError:
            raise 

        except Exception as e:
            logger.error(f"Database error while finding product: {e}")
            raise DatabaseUnavailableError("Database unavailable") from e 

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
                ProductMapper.from_document(d)
                for d in docs
            ]

       

        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            raise DatabaseUnavailableError("Database unavailable") from e

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
                raise ProductNotFoundError("Product not found")

            logger.info("Product updated successfully")

        except ServiceError:
            raise

        except Exception as e:
            logger.error(f"Database error while updating product: {e}")
            raise DatabaseUnavailableError("Database unavailable") from e 

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
                raise ProductNotFoundError("Product not found")

            logger.info("Product deleted successfully")

        except ServiceError:
            raise

        except Exception as e:
            logger.error(f"Database error while deleting product: {e}")
            raise DatabaseUnavailableError("Database unavailable") from e

    def decrease_stock(self, product_id: str, quantity: int):
        try:
            logger.info(f"Decreasing stock: {product_id}")

            doc = self.collection.find_one({"_id": product_id})

            if not doc:
                raise ProductNotFoundError("Product not found")

            if doc["quantity"] < quantity:
                raise InsufficientStockError("Insufficient stock")

            self.collection.update_one(
                {"_id": product_id},
                {
                    "$inc": {"quantity": -quantity},
                    "$set": {"updated_at": datetime.now(timezone.utc)}
                }
            )
            logger.info("Stock updated successfully")

        except ServiceError:
            raise

        except Exception as e:
            logger.error(f"Database error while decreasing stock: {e}")
            raise DatabaseUnavailableError("Database unavailable") from e 
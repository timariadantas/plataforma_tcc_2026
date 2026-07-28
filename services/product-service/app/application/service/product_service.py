from datetime import datetime, timezone
from application.mapper.product_mapper import ProductMapper
from domain.repositories.product_repository_interface import ProductRepositoryInterface
from infrastructure.logging.logger import get_logger
from infrastructure.errors.service_errors import InvalidProductDataError



logger = get_logger(__name__)


class ProductService:

    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    def create_product(self, dto, user_id):
        logger.info("Creating product")

        if dto.price <= 0:
            raise InvalidProductDataError("Price must be greater than zero")

        if dto.quantity < 0:
            raise InvalidProductDataError("Quantity cannot be negative")

        product = ProductMapper.to_entity(dto)
        
        product.created_by = user_id   # id do token

        self.repository.save(product)

        return ProductMapper.to_response(product)

    def get_all_products(self, page, limit):
        logger.info("Fetching products")

        products = self.repository.find_all(page, limit)

        return [ProductMapper.to_response(p) for p in products]

    def get_product_by_id(self, product_id):
        logger.info(f"Fetching product: {product_id}")

        product = self.repository.find_by_id(product_id)

        return ProductMapper.to_response(product)

    def update_product(self, product_id, dto):
        logger.info(f"Updating product: {product_id}")

        data = dto.model_dump()
        data["updated_at"] = datetime.now(timezone.utc)

        self.repository.update(product_id, data)

    def delete_product(self, product_id):
        logger.info(f"Deleting product: {product_id}")

        self.repository.delete(product_id)

    def decrease_stock(self, product_id, quantity):
        logger.info(f"Decreasing stock: {product_id}")

        if quantity <= 0:
            raise InvalidProductDataError("Quantity must be greater than zero")

        self.repository.decrease_stock(product_id, quantity)
from datetime import datetime
from application.mapper.product_mapper import ProductMapper
from domain.entities.product import Product
from domain.repositories.product_repository_interface import ProductRepositoryInterface
from infrastructure.logging.logger import logger
from api.dto.request.product_request_dto import ProductRequestDto


class ProductService:

    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    def create_product(self, data:ProductRequestDto):
        logger.info("Creating product")
        if data.price <= 0:
            logger.warning("Invalid price")
            raise ValueError("Price must be greater than zero")

        if data.quantity < 0:
            logger.warning("Invalid quantity")
            raise ValueError("Quantity cannot be negative")

        product = ProductMapper.to_entity(data)
        self.repository.save(product)
        logger.info("Product created successfully")
        
        return ProductMapper.to_response(product.to_dict())

    def get_all_products(self, page, limit):
        logger.info("Fetching all products")
        products = self.repository.get_all(page, limit) 
        
        logger.info(f"Total products found: {len(products)}")
        return [ProductMapper.to_response(p) for p in products]
    

    def get_product_by_id(self, product_id):
        logger.info(f"Fetching product by id: {product_id}")
        product = self.repository.get_by_id(product_id)
        return ProductMapper.to_response(product)

    def update_product(self, product_id, dto):
        logger.info(f"Updating product: {product_id}")
        
        entity = ProductMapper.to_entity(dto)
        update_data = entity.to_dict()
        update_data["updated_at"] = datetime.now()

        logger.info(f"Product updated successfully: {product_id}")
        self.repository.update(product_id, update_data)

    def delete_product(self, product_id):
        logger.info(f"Deletingcode product: {product_id}")
        self.repository.delete(product_id)
        
        logger.info(f"Product deleted successfully: {product_id}")
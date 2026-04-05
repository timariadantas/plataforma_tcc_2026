from datetime import datetime
from app.domain.entities.product import Product
from app.domain.repositories.product_repository_interface import ProductRepositoryInterface


class ProductService:

    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    def create_product(self, data):
        if data.price <= 0:
            raise Exception("Price must be greater than zero")

        if data.quantity < 0:
            raise Exception("Quantity cannot be negative")

        product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            quantity=data.quantity
        )

        self.repository.save(product)
        return product.to_dict()

    def get_all_products(self):
        return self.repository.get_all()

    def get_product_by_id(self, product_id):
        product = self.repository.get_by_id(product_id)

        if not product:
            raise Exception("Product not found")

        return product

    def update_product(self, product_id, data):
        update_data = data.__dict__
        update_data["updated_at"] = datetime.utcnow()

        self.repository.update(product_id, update_data)

    def delete_product(self, product_id):
        self.repository.delete(product_id)
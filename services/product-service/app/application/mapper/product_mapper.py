from domain.entities.product import Product

class ProductMapper:

    @staticmethod
    def to_entity(dto):
        return Product(
            name=dto.name,
            description=dto.description,
            price=dto.price,
            quantity=dto.quantity,
            active=True
        )

    @staticmethod
    def to_document(product: Product):
        return {
            "_id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "active": product.active
        }

    @staticmethod
    def from_document(doc):
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

    @staticmethod
    def to_response(product: Product):
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity
        }
from datetime import datetime
import uuid

class Product:
    def __init__(self, name, description, price, quantity):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.active = True

    def to_dict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "active": self.active
        }
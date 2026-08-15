from datetime import datetime, timezone
import ulid 

class Product:
    def __init__(
        self,
        name,
        description,
        price,
        quantity,
        id=None,
        created_at=None,
        updated_at=None,
        active=True
    ):
    
        if not name or name.strip() == "":
            raise ValueError("Name cannot be empty")

        if price <= 0:
            raise ValueError("Price must be greater than zero")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        self.id = id or str(ulid.new())
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
        self.active = active
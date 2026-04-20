class ProductMapper:
    @staticmethod
    def to_entity(dto):
        from domain.entities.product import Product
        
        return Product(
            dto.name,
            dto.description,
            dto.price,
            dto.quantity
        )
    @staticmethod
    def to_response(product_dict):
        return {
            "id" : product_dict.get("id"),
            "name" : product_dict["name"],
            "description" : product_dict["description"],
            "price" : product_dict["price"],
            "quantity" : product_dict["quantity"]
        }
        
# MONGO _id -> API id
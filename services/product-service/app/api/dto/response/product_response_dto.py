from pydantic import BaseModel 

class ProductResponseDto(BaseModel):
    id : str
    name : str
    description: str | None
    price: float
    quantity: int
    
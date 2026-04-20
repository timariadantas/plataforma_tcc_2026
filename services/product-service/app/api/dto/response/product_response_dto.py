from pydantic import BaseModel , Field

class ProductResponseDto(BaseModel):
    id : str
    name : str
    description: str | None
    price: float
    quantity: int
    
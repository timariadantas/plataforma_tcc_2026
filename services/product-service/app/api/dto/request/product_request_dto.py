from pydantic import BaseModel , Field

class ProductRequestDto(BaseModel):
    name: str = Field(...,min_length=1)
    description : str | None = None
    price : float
    quantity : int
    
    
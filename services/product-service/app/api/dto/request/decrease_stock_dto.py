from pydantic import BaseModel, Field

class DecreaseStockDto(BaseModel):
    quantity: int = Field(..., gt=0)
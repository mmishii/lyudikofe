from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class PriceSchema(BaseModel):
    id: UUID
    price: float
    volume: int
    product_id: UUID
    created_at: datetime
    updated_at: datetime

class CreatePriceSchema(BaseModel):
    price: float
    volume: int
    product_id: UUID

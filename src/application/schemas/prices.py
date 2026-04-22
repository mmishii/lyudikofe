from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class PriceSchema(BaseModel):
    id: UUID
    price: float
    volume: int
    drink_id: UUID|None = None
    food_id: UUID| None = None
    created_at: datetime
    updated_at: datetime

class CreatePriceSchema(BaseModel):
    price: float
    volume: int
    drink_id: UUID|None = None
    food_id: UUID| None = None

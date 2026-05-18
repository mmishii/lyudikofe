from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CartSchema(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    price_id: UUID
    quantity: int
    created_at: datetime
    updated_at: datetime

class CreateCartSchema(BaseModel):
    user_id: UUID
    product_id: UUID
    price_id: UUID
    quantity: int


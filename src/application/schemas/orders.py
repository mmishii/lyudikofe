from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class OrderSchema(BaseModel):
    id: UUID
    user_id: UUID
    status: str
    count: int
    price: float
    comment: str
    payment_method: str
    created_at: datetime
    updated_at: datetime

class CreateOrderSchema(BaseModel):
    id: UUID
    user_id: UUID
    status: str
    count: int
    price: float
    comment: str
    payment_method: str
    
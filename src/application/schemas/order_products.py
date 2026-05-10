from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class OrderProductSchema(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float
    created_at: datetime
    updated_at: datetime

class CreateOrderProductSchema(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float
    
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CustomCartSchema(BaseModel):
    id: UUID
    cart_product_id: UUID
    ingredient_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateCustomCartSchema(BaseModel):
    cart_drink_id: UUID
    ingredient_id: UUID

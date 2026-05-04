from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CustomCartProductSchema(BaseModel):
    id: UUID
    cart_drink_id: UUID
    ingredient_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateCustomCartProductSchema(BaseModel):
    cart_drink_id: UUID
    ingredient_id: UUID

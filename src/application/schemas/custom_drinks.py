from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CustomDrinkSchema(BaseModel):
    id: UUID
    cart_drink_id: UUID
    ingredient_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateCustomDrinkSchema(BaseModel):
    cart_drink_id: UUID
    ingredient_id: UUID

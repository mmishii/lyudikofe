from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class FoodSchema(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    is_available: bool
    category: str
    macros_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateFoodSchema(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool
    category: str
    macros_id: UUID

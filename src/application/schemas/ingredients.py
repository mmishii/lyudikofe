from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class IngredientSchema(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    is_available: bool
    category: str
    macros_id: UUID
    created_at: datetime
    updated_at: datetime


class CreateIngredientSchema(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool
    category: str
    macros_id: UUID

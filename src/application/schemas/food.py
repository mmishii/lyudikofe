from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class FoodSchema(BaseModel):
    id: UUID
    name: str
    description: str|None = None
    ingredients: str|None = None
    is_available: bool
    category: str|None = None
    macros_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateFoodSchema(BaseModel):
    name: str
    description: str|None = None
    ingredients: str|None = None
    is_available: bool
    category: str|None = None
    macros_id: UUID

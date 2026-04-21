from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class DrinkSchema(BaseModel):
    id: UUID
    name: str
    description: str
    is_available: bool
    category: str
    season: str
    macros_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateDrinkSchema(BaseModel):
    name: str
    description: str
    is_available: bool
    category: str
    season: str
    macros_id: UUID

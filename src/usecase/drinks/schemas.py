from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class RequestDrink(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool
    category: str
    season: str
    volume: int
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float

class ResponseDrink(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    is_available: bool
    category: str
    season: str
    macros_id: UUID
    volume: int
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float
    created_at: datetime
    updated_at: datetime

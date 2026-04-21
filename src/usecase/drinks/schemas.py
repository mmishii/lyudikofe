from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ApiPriceSchema(BaseModel):
    volume: int
    price: float


class RequestDrink(BaseModel):
    name: str
    description: str
    prices: list[ApiPriceSchema]
    is_available: bool
    category: str
    season: str
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float

class ResponseDrink(BaseModel):
    id: UUID
    name: str
    description: str
    prices: list[ApiPriceSchema]
    is_available: bool
    category: str
    season: str
    macros_id: UUID
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float
    created_at: datetime
    updated_at: datetime

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ApiPriceSchema(BaseModel):
    volume: int
    price: float


class RequestDrink(BaseModel):
    name: str
    description: str|None = None
    ingredients: str|None = None
    prices: list[ApiPriceSchema]
    is_available: bool
    image_name: str
    category: str|None = None
    season: str|None = None
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float

class ResponseDrink(BaseModel):
    id: UUID
    name: str
    description: str|None = None
    ingredients: str|None = None
    prices: list[ApiPriceSchema]
    is_available: bool
    category: str|None = None
    season: str|None = None
    image_url: str
    macros_id: UUID
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float
    created_at: datetime
    updated_at: datetime

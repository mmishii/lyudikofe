from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ApiPriceSchema(BaseModel):
    volume: int
    price: float


class RequestFood(BaseModel):
    name: str
    description: str|None = None
    ingredients: str|None = None
    prices: list[ApiPriceSchema]
    is_available: bool
    image_name: str
    category: str|None = None
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float

class ResponseFood(BaseModel):
    id: UUID
    name: str
    description: str|None = None
    ingredients: str|None = None
    prices: list[ApiPriceSchema]
    is_available: bool
    category: str|None = None
    image_url: str|None = None
    created_at: datetime
    updated_at: datetime



class ResponseAllFood(ResponseFood):
    macros_id: UUID
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float

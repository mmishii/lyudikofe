from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ApiPriceSchema(BaseModel):
    volume: int
    price: float

class ResponseIngredients(BaseModel):
    id: UUID
    name: str
    description: str|None = None
    prices: float
    is_available: bool
    category: str|None = None
    image_url: str
    created_at: datetime
    updated_at: datetime


class ResponseAllIngredients(ResponseIngredients):
    macros_id: UUID
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float
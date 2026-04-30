from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ApiPriceSchema(BaseModel):
    volume: int
    price: float


class RequestProduct(BaseModel):
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


class MacrosSchema(BaseModel):
    volume: int
    price: float
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float

class ResponseProducts(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    ingredients: str | None = None
    prices: list[MacrosSchema]
    is_available: bool
    category: str | None = None
    season: str | None = None
    image_url: str
    created_at: datetime
    updated_at: datetime



class ResponseProduct(ResponseProducts):
    macros_id: UUID
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float


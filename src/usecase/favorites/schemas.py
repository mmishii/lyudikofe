from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from src.application.schemas.custom_favorites import CustomFavoritesSchema

class RequestCustomFavoritesSchema(BaseModel):
    ingredient_id: UUID
    price_id: UUID

class RequestCreateFavoritesSchema(BaseModel):
    product_id: UUID
    price_id: UUID
    custom: list[RequestCustomFavoritesSchema]

class ResponseCustomFavoritesSchema(BaseModel):
    id: UUID
    user_id: UUID
    price_id: UUID
    product_id: UUID
    customs: list[CustomFavoritesSchema]
    created_at: datetime
    updated_at: datetime

class GetFavorioteProductsSchema(BaseModel):
    id: UUID
    image_url: str
    name: str
    is_available: bool
    price_id: UUID
    price: float
    volume: int

class GetFavoritesSchema(BaseModel):
    id: UUID
    user_id: UUID
    products: GetFavorioteProductsSchema
    created_at: datetime
    updated_at: datetime


class GetCustomFavoritesSchema(BaseModel):
    ingredient_id: UUID
    price_id: UUID
    volume: int
    price:float
    name: str

class ResponseGetFavoritesSchema(BaseModel):
    customs: list[GetCustomFavoritesSchema]
    id: UUID
    user_id: UUID
    products: GetFavorioteProductsSchema
    created_at: datetime
    updated_at: datetime


from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from src.application.schemas.custom_favorites import CustomFavoritesSchema

class RequestCustomFavoritesSchema(BaseModel):
    ingredient_id: UUID

class RequestCreateFavoritesSchema(BaseModel):
    user_id: UUID
    product_id: UUID
    custom: list[RequestCustomFavoritesSchema]

class ResponseCustomFavoritesSchema(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    customs: list[CustomFavoritesSchema]
    created_at: datetime
    updated_at: datetime

class GetFavoritesSchema(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    name: str
    image_url: str
    created_at: datetime
    updated_at: datetime


class GetCustomFavoritesSchema(BaseModel):
    ingredient_id: UUID
    name: str

class ResponseGetFavoritesSchema(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    name: str
    image_url: str
    customs: list[GetCustomFavoritesSchema]
    created_at: datetime
    updated_at: datetime


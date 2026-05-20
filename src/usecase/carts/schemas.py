from pydantic import BaseModel
from uuid import UUID
from src.application.schemas.custom_cart_products import CustomCartSchema
from src.usecase import products
from datetime import datetime


class RequestCustomCartProducts(BaseModel):
    ingredient_id: UUID
    price_id: UUID

class RequestCartProducts(BaseModel):
    product_id: UUID
    quantity: int
    price_id: UUID
    customs: list[RequestCustomCartProducts]


class ResponseCartProducts(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    price_id: UUID
    customs: list[CustomCartSchema]|None = None
    quantity: int
    created_at: datetime
    updated_at: datetime

class PriceSchema(BaseModel):
    id: UUID
    price: float
    volume: int
    created_at: datetime
    updated_at: datetime

class ProductSchema(BaseModel):
    id: UUID
    name: str
    is_available: bool
    image_url: str
    price:PriceSchema
    customs: list[CustomCartSchema]|None = None
    created_at: datetime
    updated_at: datetime

class CustomSchema(BaseModel):
    id: UUID
    name: str | None = None


class CustomCartSchema(BaseModel):
    id: UUID
    ingredient_id: UUID
    cart_product_id: UUID
    price:PriceSchema
    created_at: datetime
    updated_at: datetime

class CartProductsSchema(BaseModel):
    id: UUID
    user_id: UUID
    products: ProductSchema
    customs: list[CustomCartSchema]|None = None
    quantity: int
    created_at: datetime
    updated_at: datetime

class ResponseProductsSchema(BaseModel):
    id: UUID
    name: str
    price: float
    is_available: bool
    image: str
    customs: list[CustomSchema]|None = None
    created_at: datetime
    updated_at: datetime

class ResponseCartProductsSchema(BaseModel):
    id: UUID
    user_id: UUID
    products: ResponseProductsSchema
    quantity: int
    created_at: datetime
    updated_at: datetime
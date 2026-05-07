from pydantic import BaseModel
from uuid import UUID
from src.application.schemas.custom_cart_products import CustomCartSchema
from src.usecase import products


class RequestCustomCartProducts(BaseModel):
    ingredient_id: UUID

class RequestCartProducts(BaseModel):
    product_id: UUID
    quantity: int
    customs: list[RequestCustomCartProducts]


class ResponseCartProducts(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    customs: list[CustomCartSchema]|None = None
    quantity: int
    created_at: str
    updated_at: str

class ProductSchema(BaseModel):
    id: UUID
    name: str
    is_available: bool
    price: float
    image: str
    ingredient_id: UUID|None = None

class CustomSchema(BaseModel):
    id: UUID
    name: str | None = None


class CustomCartSchema(BaseModel):
    ingredient_id: UUID

class CartProductsSchema(BaseModel):
    id: UUID
    user_id: UUID
    products: ProductSchema
    image: str
    customs: list[CustomCartSchema]|None = None
    quantity: int
    created_at: str
    updated_at: str

class ResponseProductsSchema(BaseModel):
    id: UUID
    name: str
    price: float
    is_available: bool
    image: str
    customs: list[CustomSchema]|None = None

class ResponseCartProductsSchema(BaseModel):
    id: UUID
    user_id: UUID
    products: ResponseProductsSchema
    quantity: int
    created_at: str
    updated_at: str
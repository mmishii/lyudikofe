from pydantic import BaseModel
from uuid import UUID
from src.application.schemas.custom_order import CustomOrderProductSchema
from src.application.schemas.orders import OrderSchema
from src.application.schemas.order_products import OrderProductSchema

class RequestCustomOrderProductSchema(BaseModel):
    id: UUID
    ingredient_id: UUID
    order_product_id: UUID

class RequestOrderProduct(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float
    custom_products: list[RequestCustomOrderProductSchema]

class RequestOrderSchema(BaseModel):
    status: str
    count: int
    price: float
    comment: str
    payment_method: str
    products: list[RequestOrderProduct]

class ResponseProductSchema(OrderProductSchema):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float
    custom_products: list[CustomOrderProductSchema]

class ResponseOrderSchema(OrderSchema):
    products: list[ResponseProductSchema]

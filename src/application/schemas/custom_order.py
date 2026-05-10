from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CustomOrderProductSchema(BaseModel):
    id: UUID
    ingredient_id: UUID
    order_product_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateCustomOrderProductSchema(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    
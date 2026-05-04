from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CartProductsSchema(BaseModel):
    id: UUID
    user_id: UUID
    drink_id: UUID
    quantity: UUID
    created_at: datetime
    updated_at: datetime

class CreateCartProductsSchema(BaseModel):
    user_id: UUID
    drink_id: UUID
    quantity: UUID


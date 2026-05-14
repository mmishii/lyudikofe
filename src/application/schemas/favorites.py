from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class FavoritesSchema(BaseModel):
    id: UUID
    user_id: UUID
    price_id: UUID
    product_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateFavoritesSchema(BaseModel):
    price_id: UUID
    user_id: UUID
    product_id: UUID
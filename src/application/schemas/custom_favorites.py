from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CustomFavoritesSchema(BaseModel):
    id: UUID
    ingredient_id: UUID
    favorite_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateCustomFavoritesSchema(BaseModel):
    ingredient_id: UUID
    favorite_id: UUID
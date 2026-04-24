from datetime import datetime
from uuid import UUID
from src.application.schemas.common import BaseModel


class ImageSchema(BaseModel):
    id: UUID
    name: str
    drink_id: UUID|None = None
    food_id: UUID|None = None
    created_at: datetime
    updated_at: datetime


class CreateImageSchema(BaseModel):
    name: str
    drink_id: UUID|None = None
    food_id: UUID|None = None


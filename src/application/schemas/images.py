from datetime import datetime
from uuid import UUID
from src.application.schemas.common import BaseModel


class ImageSchema(BaseModel):
    id: UUID
    name: str
    product_id: UUID
    created_at: datetime
    updated_at: datetime


class CreateImageSchema(BaseModel):
    name: str
    product_id: UUID

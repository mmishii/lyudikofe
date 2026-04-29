from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class UserSchemas(BaseModel):
    id: UUID
    name: str
    phone: int
    email: str
    created_at: datetime
    updated_at: datetime

class CreateUserSchema(BaseModel):
    id: UUID
    name: str
    phone: int
    email: str

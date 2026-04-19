from datetime import datetime
from src.application.schemas.common import BaseModel

class StringSchema(BaseModel):
    name: str
    created_at: datetime
    updated_at: datetime

    
class CreateStringSchema(BaseModel):
    name: str
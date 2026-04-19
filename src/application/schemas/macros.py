from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class MacrosSchema(BaseModel):
    id: UUID
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float
    created_at: datetime
    updated_at: datetime

class CreateMacrosSchema(BaseModel):
    unit_kkal: float
    unit_proteins: float
    unit_carbs: float
    unit_fats: float

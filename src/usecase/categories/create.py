from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.application.schemas.string import CreateStringSchema, StringSchema
from src.infra.postgres.tables import CategoriesModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateCategoryUsecase(Usecase[CreateStringSchema, StringSchema]):
    session: AsyncSession
    create_category: CreateReturningGate[CategoriesModel, CreateStringSchema, StringSchema]

    async def __call__(self, data: CreateStringSchema) -> StringSchema:
        async with self.session.begin():
            category = await self.create_category(data)
        return category
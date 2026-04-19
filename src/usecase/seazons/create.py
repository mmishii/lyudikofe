from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.application.schemas.string import CreateStringSchema, StringSchema
from src.infra.postgres.tables import SeasonsModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateSeasonUsecase(Usecase[CreateStringSchema, StringSchema]):
    session: AsyncSession
    create_season: CreateReturningGate[SeasonsModel, CreateStringSchema, StringSchema]

    async def __call__(self, data: CreateStringSchema) -> StringSchema:
        async with self.session.begin():
            season = await self.create_season(data)
        return season
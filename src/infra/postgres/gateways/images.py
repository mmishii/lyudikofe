from http.client import responses

from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from uuid import UUID
from src.infra.postgres.tables import FoodModel, MacrosModel, PricesModel, ImagesModel
from src.usecase.food.schemas import ResponseFood
from sqlalchemy import select, or_, literal
from src.application.errors import NotFoundError


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetImageNameGateway(PostgresGateway):
    async def __call__(self, id_product: UUID) -> str:
        stmt = select(ImagesModel.name,
                      ImagesModel.drink_id,
                      ImagesModel.food_id).where(or_(
                        ImagesModel.drink_id == id_product,
                        ImagesModel.food_id == id_product,
                    ))
        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise NotFoundError(table=ImagesModel)
        return result.name
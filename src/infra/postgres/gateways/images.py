from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from uuid import UUID
from src.infra.postgres.tables import ImageFoodsModel, ImageDrinksModel
from sqlalchemy import select
from src.application.errors import NotFoundError


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetImageDrinkNameGateway(PostgresGateway):
    async def __call__(self, product_id: UUID) -> str:
        stmt = select(ImageDrinksModel.name,
                      ImageDrinksModel.drink_id).where(
                        ImagesModel.drink_id == product_id,
                    )
        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise NotFoundError(table=ImagesModel)
        return result.name

@dataclass(slots=True, kw_only=True)
class GetImageFoodNameGateway(PostgresGateway):
    async def __call__(self, product_id: UUID) -> str:
        stmt = select(ImageFoodsModel.name,
                      ImageFoodsModel.food_id).where(
                        ImageFoodsModel.food_id == product_id,
                    )
        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise NotFoundError(table=ImagesModel)
        return result.name
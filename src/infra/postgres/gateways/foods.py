from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.infra.postgres.tables import FoodModel, MacrosModel, PricesModel, ImagesModel
from src.usecase.food.schemas import ResponseFood, ResponseAllFood
from sqlalchemy import select, func, literal
from src.application.errors import NotFoundError
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetFoodsGateway(PostgresGateway):
    async def __call__(self, category: str) -> list[ResponseFood]:
        stmt = (select(
            FoodModel.id,
            FoodModel.name,
            FoodModel.description,
            FoodModel.is_available,
            FoodModel.ingredients,
            FoodModel.category,
            func.concat(
                PricesModel.price,
                PricesModel.volume
            ).label('price'),
            FoodModel.created_at,
            FoodModel.updated_at
        )
            .join(PricesModel, PricesModel.food_id == FoodModel.id)
                .where(FoodModel.category == category))

        result = (await self.session.execute(stmt)).mappings().fetchall()
        if result is None:
            raise NotFoundError(table=FoodModel)
        return [ResponseFood.model_validate(row) for row in result]


@dataclass(slots=True, kw_only=True)
class GetFoodsByIdGateway(PostgresGateway):
    async def __call__(self, data_id: UUID) -> list[ResponseAllFood]:
        stmt = (select(
            FoodModel.id,
            FoodModel.name,
            FoodModel.description,
            FoodModel.ingredients,
            FoodModel.is_available,
            FoodModel.category,
            MacrosModel.unit_kkal,
            MacrosModel.unit_fats,
            MacrosModel.unit_carbs,
            MacrosModel.unit_proteins,
            func.concat(
                PricesModel.price,
                PricesModel.volume
            ).label('price'),
            FoodModel.created_at,
            FoodModel.updated_at
        )
                .join(PricesModel, PricesModel.drink_id == FoodModel.id)
                .join(MacrosModel, MacrosModel.id == FoodModel.macros_id)
                .where(FoodModel.id == data_id))

        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise NotFoundError(table=FoodModel)
        return [ResponseAllFood.model_validate(row) for row in result]

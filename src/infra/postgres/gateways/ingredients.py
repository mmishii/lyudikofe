from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.infra.postgres.tables import MacrosModel, PricesModel, ImagesModel, IngredientsModel
from src.usecase.ingredients.schemas import ResponseIngredients, ResponseAllIngredients
from sqlalchemy import select, func, literal
from src.application.errors import NotFoundError
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetIngredientsGateway(PostgresGateway):
    async def __call__(self, category: str) -> list[ResponseIngredients]:
        stmt = (select(
            IngredientsModel.id,
            IngredientsModel.name,
            IngredientsModel.description,
            IngredientsModel.is_available,
            IngredientsModel.category,
            IngredientsModel.price,
            IngredientsModel.created_at,
            IngredientsModel.updated_at
        )
                .where(IngredientsModel.category == category))

        result = (await self.session.execute(stmt)).mappings().fetchall()
        if result is None:
            raise NotFoundError(table=IngredientsModel)
        return [ResponseIngredients.model_validate(row) for row in result]


@dataclass(slots=True, kw_only=True)
class GetIngredientByIdGateway(PostgresGateway):
    async def __call__(self, data_id: UUID) -> list[ResponseAllIngredients]:
        stmt = (select(
            IngredientsModel.id,
            IngredientsModel.name,
            IngredientsModel.description,
            IngredientsModel.is_available,
            IngredientsModel.category,
            MacrosModel.unit_kkal,
            MacrosModel.unit_fats,
            MacrosModel.unit_carbs,
            MacrosModel.unit_proteins,
            func.concat(
                PricesModel.price,
                PricesModel.volume
            ).label('price'),
            IngredientsModel.created_at,
            IngredientsModel.updated_at
        )
                .join(PricesModel, PricesModel.drink_id == IngredientsModel.id)
                .join(MacrosModel, MacrosModel.id == IngredientsModel.macros_id)
                .where(IngredientsModel.id == data_id))

        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise NotFoundError(table=IngredientsModel)
        return [ResponseAllIngredients.model_validate(row) for row in result]

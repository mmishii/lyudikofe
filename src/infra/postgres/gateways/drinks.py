from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.infra.postgres.tables import DrinksModel, MacrosModel, PricesModel, ImagesModel
from src.usecase.drinks.schemas import ResponseDrink, ResponseAllDrink
from sqlalchemy import select, func, literal
from src.application.errors import NotFoundError
from uuid import UUID

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetDrinksGateway(PostgresGateway):
    async def __call__(self, category: str) -> list[ResponseDrink]:
        stmt = (select(
                DrinksModel.id,
                DrinksModel.name,
                DrinksModel.description,
                DrinksModel.ingredients,
                DrinksModel.is_available,
                DrinksModel.category,
                DrinksModel.season,
                func.concat(
                    PricesModel.price,
                    PricesModel.volume
                ).label('price'),
                DrinksModel.created_at,
                DrinksModel.updated_at
            )
            .join(PricesModel, PricesModel.drink_id == DrinksModel.id)
            .where(DrinksModel.category==category))


        result = (await self.session.execute(stmt)).mappings().fetchall()
        if result is None:
            raise NotFoundError(table=DrinksModel)
        return [ResponseDrink.model_validate(row) for row in result]
    

@dataclass(slots=True, kw_only=True)
class GetDrinksByIdGateway(PostgresGateway):
    async def __call__(self, data_id: UUID) -> ResponseAllDrink:
        stmt = (select(
                DrinksModel.id,
                DrinksModel.name,
                DrinksModel.description,
                DrinksModel.ingredients,
                DrinksModel.is_available,
                DrinksModel.category,
                DrinksModel.season,
                MacrosModel.unit_kkal,
                MacrosModel.unit_fats,
                MacrosModel.unit_carbs,
                MacrosModel.unit_proteins,
                func.concat(
                    PricesModel.price,
                    PricesModel.volume
                ).label('price'),
                DrinksModel.created_at,
                DrinksModel.updated_at
            )
            .join(PricesModel, PricesModel.drink_id == DrinksModel.id)
            .join(MacrosModel, MacrosModel.id == DrinksModel.macros_id)
                .where(DrinksModel.id == data_id))


        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise NotFoundError(table=DrinksModel)
        return ResponseAllDrink.model_validate(result)

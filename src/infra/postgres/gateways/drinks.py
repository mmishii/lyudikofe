from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.infra.postgres.tables import DrinksModel, MacrosModel
from src.usecase.drinks.schemas import ResponseDrink
from sqlalchemy import select, and_, func
from src.application.services.pagination import Pagination
from src.application.errors import NotFoundError
from src.application.schemas.common import ResponsePaginationSchema

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetDrinksGateway(PostgresGateway):
    pagination: Pagination
    async def __call__(self, limit: int, offset: int) -> ResponsePaginationSchema[ResponseDrink]:
        stmt = (select(
                DrinksModel.id,
                DrinksModel.name,
                DrinksModel.description,
                DrinksModel.price,
                DrinksModel.is_available,
                DrinksModel.category,
                DrinksModel.season,
                DrinksModel.macros_id,
                DrinksModel.volume,
                MacrosModel.unit_kkal,
                MacrosModel.unit_proteins,
                MacrosModel.unit_carbs,
                MacrosModel.unit_fats,
                DrinksModel.created_at,
                DrinksModel.updated_at
            )
            .join(MacrosModel, MacrosModel.id == DrinksModel.macros_id))
        result = (await self.session.execute(stmt)).mappings().fetchall()
        if result is None:
            raise NotFoundError(table=DrinksModel)
        result = [ResponseDrink.model_validate(row) for row in result]
        return self.pagination(result, limit, offset, ResponseDrink)
    

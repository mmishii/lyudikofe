from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.drinks import GetDrinksGateway
from src.usecase.drinks.schemas import RequestDrink, ResponseDrink
from src.application.schemas.common import ResponsePaginationSchema, PaginationSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class GetDrinksUsecase(Usecase[PaginationSchema, ResponsePaginationSchema[ResponseDrink]]):
    session: AsyncSession
    get_drink: GetDrinksGateway
    
    async def __call__(self, data: PaginationSchema) -> ResponsePaginationSchema[ResponseDrink]:
        async with self.session.begin():
            return await self.get_drink(limit=data.limit, offset=data.offset)
            
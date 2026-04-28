from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.drinks import GetDrinksGateway
from src.usecase.drinks.schemas import ResponseDrink
from src.infra.postgres.gateways.images import GetImageNameGateway
from src.application.schemas.common import ResponsePaginationSchema, RequestPaginationSchema
from src.application.services.pagination import Pagination
from dataclasses import dataclass
from src.infra.minio.get import GetImg

@dataclass(slots=True, frozen=True, kw_only=True)
class GetDrinksUsecase(Usecase[RequestPaginationSchema, ResponsePaginationSchema[ResponseDrink]]):
    session: AsyncSession
    get_drink: GetDrinksGateway
    pagination: Pagination[ResponseDrink]
    get_img_url: GetImageNameGateway
    get_img: GetImg
    
    async def __call__(self, data: RequestPaginationSchema) -> ResponsePaginationSchema[ResponseDrink]:
        async with self.session.begin():
            drinks = await self.get_drink(category=data.category)
            for i in range(len(drinks)):
                drinks[i].image_url = await self.get_img_url(drinks[i].id)
                drinks[i].image_url = await self.get_img(drinks[i].image_url)
            return self.pagination(
                items=drinks,
            limit=data.limit,
            offset=data.offset,
            schema_class=ResponseDrink)
            
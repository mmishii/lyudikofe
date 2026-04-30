from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.foods import GetFoodsGateway
from src.usecase.food.schemas import ResponseFood
from src.application.schemas.common import ResponsePaginationSchema, RequestPaginationSchema
from src.application.services.pagination import Pagination
from src.infra.postgres.gateways.images import GetImageDrinkNameGateway
from src.infra.minio.get import GetImg
from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class GetFoodUsecase(Usecase[RequestPaginationSchema, ResponsePaginationSchema[ResponseFood]]):
    session: AsyncSession
    get_foods: GetFoodsGateway
    pagination: Pagination[ResponseFood]
    get_img: GetImageDrinkNameGateway
    get_img_url: GetImg

    async def __call__(self, data: RequestPaginationSchema) -> ResponsePaginationSchema[ResponseFood]:
        async with self.session.begin():
            foods = await self.get_foods(category=data.category)
            for i in range(len(foods)):
                foods[i].image_url = await self.get_img(foods[i].id)
                foods[i].image_url = await self.get_img_url(foods[i].image_url)
            return self.pagination(
                items=foods,
                limit=data.limit,
                offset=data.offset,
                schema_class=ResponseFood)

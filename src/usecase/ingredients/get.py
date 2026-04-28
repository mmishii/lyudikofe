from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.ingredients import GetIngredientsGateway
from src.usecase.ingredients.schemas import ResponseIngredients
from src.application.schemas.common import ResponsePaginationSchema, RequestPaginationSchema
from src.application.services.pagination import Pagination
from src.infra.postgres.gateways.images import GetImageNameGateway
from dataclasses import dataclass
from src.infra.minio.get import GetImg


@dataclass(slots=True, frozen=True, kw_only=True)
class GetIngredientsUsecase(Usecase[RequestPaginationSchema, ResponsePaginationSchema[ResponseIngredients]]):
    session: AsyncSession
    get_ingredients: GetIngredientsGateway
    pagination: Pagination[ResponseIngredients]
    get_img: GetImageNameGateway
    get_img_url: GetImg

    async def __call__(self, data: RequestPaginationSchema) -> ResponsePaginationSchema[ResponseIngredients]:
        async with self.session.begin():
            ingredients = await self.get_ingredients(category=data.category)
            for i in range(len(ingredients)):
                ingredients[i].image_url = await self.get_img(ingredients[i].id)
                ingredients[i].image_url = await self.get_img_url(ingredients[i].image_url)
            return self.pagination(
                items=ingredients,
                limit=data.limit,
                offset=data.offset,
                schema_class=ResponseIngredients)

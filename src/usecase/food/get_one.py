from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.foods import GetFoodsByIdGateway
from src.usecase.food.schemas import ResponseAllFood
from src.infra.postgres.gateways.images import GetImageNameGateway
from dataclasses import dataclass
from src.infra.minio.get import GetImg


@dataclass(slots=True, frozen=True, kw_only=True)
class GetFoodByIdUsecase(Usecase[UUID, ResponseAllFood]):
    session: AsyncSession
    get_food: GetFoodsByIdGateway
    get_img_url: GetImageNameGateway
    get_img: GetImg

    async def __call__(self, data_id: UUID) -> ResponseAllFood:
        async with self.session.begin():
            food = await self.get_food(data_id=data_id)
            food.image_url = await self.get_img_url(food.id)
            food.image_url = await self.get_img(food.image_url)
            return food


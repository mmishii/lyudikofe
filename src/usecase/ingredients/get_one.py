from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.ingredients import GetIngredientByIdGateway
from src.usecase.food.schemas import ResponseAllFood
from src.infra.postgres.gateways.images import GetImageNameGateway
from dataclasses import dataclass
from src.infra.minio.get import GetImg


@dataclass(slots=True, frozen=True, kw_only=True)
class GetIngredientByIdUsecase(Usecase[UUID, ResponseAllFood]):
    session: AsyncSession
    get_ingredient: GetIngredientByIdGateway
    get_img_url: GetImageNameGateway
    get_img: GetImg

    async def __call__(self, data_id: UUID) -> ResponseAllFood:
        async with self.session.begin():
            inggredient = await self.get_ingredient(data_id=data_id)
            inggredient.image_url = await self.get_img_url(inggredient.id)
            inggredient.image_url = await self.get_img(inggredient.image_url)
            return inggredient


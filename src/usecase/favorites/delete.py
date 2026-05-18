from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from uuid import UUID
from src.usecase.base import Usecase
from src.infra.postgres.gateways.favorites import GetFavoriteProductGateway, DeleteFavoriteCustomGateway
from dataclasses import dataclass



@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteFavoritesUsecase(Usecase[UUID, bool]):
    session: AsyncSession
    user: AuthSchema
    get_favorite_product_gate: GetFavoriteProductGateway
    delete_favorite_custom_gate: DeleteFavoriteCustomGateway

    async def __call__(self, product_id: UUID) -> bool:
        async with self.session.begin():
            favorite_id = await self.get_favorite_product_gate(product_id=product_id, user_id=self.user.id)
            return await self.delete_favorite_custom_gate(favorite_product_id=favorite_id)
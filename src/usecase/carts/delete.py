from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from uuid import UUID
from src.usecase.base import Usecase
from src.infra.postgres.gateways.carts import GetCartProductGateway, DeleteCartCustomGateway
from dataclasses import dataclass



@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteCartUsecase(Usecase[UUID, bool]):
    session: AsyncSession
    user: AuthSchema
    get_cart_product_gate: GetCartProductGateway
    delete_cart_custom_gate: DeleteCartCustomGateway

    async def __call__(self, product_id: UUID) -> bool:
        async with self.session.begin():
            cart_id = await self.get_cart_product_gate(product_id=product_id, user_id=self.user.id)
            return await self.delete_cart_custom_gate(cart_product_id=cart_id, user_id=self.user.id)
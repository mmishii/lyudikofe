from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from uuid import UUID
from src.usecase.base import Usecase
from src.infra.postgres.gateways.carts import DeleteCartCustomGateway
from dataclasses import dataclass



@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteCartUsecase(Usecase[UUID, bool]):
    session: AsyncSession
    user: AuthSchema
    delete_cart_custom_gate: DeleteCartCustomGateway

    async def __call__(self, cart_product_id: UUID) -> bool:
        async with self.session.begin():
            return await self.delete_cart_custom_gate(cart_product_id=cart_product_id)
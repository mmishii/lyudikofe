from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.carts import GetCartGateway
from src.infra.postgres.gateways.base import GetByIdGate
from src.infra.postgres.tables import ProductsModel, CustomsCartModel
from src.usecase.carts.schemas import CustomSchema, CartProductsSchema, ResponseCartProductsSchema
from dataclasses import dataclass
from src.infra.minio.get import GetImg



@dataclass(slots=True, frozen=True, kw_only=True)
class GetCartUsecase(Usecase[None, list[CartProductsSchema]]):
    session: AsyncSession
    user: AuthSchema
    get_cart: GetCartGateway
    get_custom: GetByIdGate[CustomsCartModel, UUID, CustomSchema]
    get_img: GetImg

    async def __call__(self, data: None=None) -> list[CartProductsSchema]:
        async with self.session.begin():
            cart = await self.get_cart(self.user.id)
            for _product in range(len(cart)):
                cart[_product].products.image_url = await self.get_img(cart[_product].products.image_url)
            return cart
            


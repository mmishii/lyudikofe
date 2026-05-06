from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.carts import GetCartGateway
from src.infra.postgres.gateways.base import GetByIdGate
from src.infra.postgres.tables import ProductsModel
from src.usecase.carts.schemas import CustomSchema, ResponseProductsSchema, ResponseCartProductsSchema
from dataclasses import dataclass
from src.infra.minio.get import GetImg



@dataclass(slots=True, frozen=True, kw_only=True)
class GetCartUsecase(Usecase[None, ResponseCartProductsSchema]):
    session: AsyncSession
    user: AuthSchema
    get_cart: GetCartGateway
    get_custom: GetByIdGate[ProductsModel, UUID, CustomSchema]
    get_img: GetImg

    async def __call__(self, data: None=None) -> ResponseCartProductsSchema:
        async with self.session.begin():
            cart = await self.get_cart(self.user.id)
            customs = []
            
            products = []
            for product in cart.products:
                customs = []
                if product.customs is not None:
                    for custom in product.customs:
                        custom_ = await self.get_custom(custom.ingredient_id)
                        customs.append(custom_)
                product.image = await self.get_img(product.image)
                products.append(ResponseProductsSchema(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    is_available=product.is_available,
                    image=product.image,
                    customs=customs
                ))
            return ResponseCartProductsSchema(
                id=cart.id,
                user_id=cart.user_id,
                products=products,
                quantity=cart.quantity,
                created_at=str(cart.created_at),
                updated_at=str(cart.updated_at),)
            


from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from uuid import UUID
from src.usecase.base import Usecase
from src.infra.postgres.tables import CartModel, CustomsCartModel, ProductsModel
from src.infra.postgres.gateways.base import CreateReturningGate, GetByIdGate
from src.application.schemas.carts import CreateCartSchema, CartSchema
from src.application.schemas.custom_cart_products import CreateCustomCartSchema, CustomCartSchema
from src.usecase.carts.schemas import RequestCartProducts, ResponseCartProducts
from src.application.schemas.products import ProductSchema
from dataclasses import dataclass



@dataclass(slots=True, frozen=True, kw_only=True)
class CreateCartUsecase(Usecase[RequestCartProducts, ResponseCartProducts|None]):
    session: AsyncSession
    user: AuthSchema
    create_cart: CreateReturningGate[CartModel, CreateCartSchema, CartSchema]
    create_custom_cart: CreateReturningGate[CustomsCartModel, CreateCustomCartSchema, CustomCartSchema]
    get_product: GetByIdGate[ProductsModel, UUID, ProductSchema]

    async def __call__(self, data: RequestCartProducts) -> ResponseCartProducts|None:
        async with self.session.begin():
            product = await self.get_product(data.product_id)
            if product.is_available == True:
                cart = await self.create_cart(
                    CreateCartSchema(
                        user_id=self.user.id,
                        product_id=data.product_id,
                        price_id=data.price_id,
                        quantity=data.quantity
                    )
                )
                customs = []
                for ingredient in data.customs:
                    custom = await self.create_custom_cart(
                        CreateCustomCartSchema(
                            cart_product_id=cart.id,
                            ingredient_id=ingredient.ingredient_id,
                            price_id=ingredient.price_id,
                        )
                    )
                    customs.append(custom)
                return ResponseCartProducts(
                    id=cart.id,
                    user_id=cart.user_id,
                    price_id=cart.price_id,
                    product_id=cart.product_id,
                    quantity=cart.quantity,
                    created_at=str(cart.created_at),
                    updated_at=str(cart.updated_at),
                    customs=customs
                )
        return None



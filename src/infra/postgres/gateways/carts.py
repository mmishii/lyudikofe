from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.infra.postgres.tables import ProductsModel, CartModel, CustomsCartModel, ImagesModel
from src.usecase.carts.schemas import CartProductsSchema, CustomSchema
from sqlalchemy import select, func, literal, delete
from src.application.errors import NotFoundError
from uuid import UUID

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetCartGateway(PostgresGateway):
    async def __call__(self, user_id: UUID) -> list[CartProductsSchema]:
        stmt = (select(
                CartModel.id,
                CartModel.user_id,
                CartModel.quantity,
                func.concat(
                    ProductsModel.id,
                    ProductsModel.name,
                    ProductsModel.price,
                    ProductsModel.is_available,
                    func.concat(
                    CustomsCartModel.ingredient_id,
                ).label('customs'),
                    ImagesModel.name
                ).label('products'),
                CartModel.created_at,
                CartModel.updated_at
            )
            .join(CartModel, CartModel.product_id == ProductsModel.id)
            .join(CustomsCartModel, CustomsCartModel.cart_product_id == CartModel.id)
            .join(ImagesModel, ImagesModel.product_id == ProductsModel.id)
            .where(CartModel.user_id == user_id))


        result = (await self.session.execute(stmt)).mappings().fetchall()
        if result is None:
            raise NotFoundError(table=ProductsModel)
        return [CartProductsSchema.model_validate(row) for row in result]


@dataclass(slots=True, kw_only=True)
class GetCartProductGateway(PostgresGateway):
    async def __call__(self, product_id: UUID, user_id: UUID) -> UUID:
        stmt = (select(
            CartModel.id,
        )
        .where(CartModel.product_id == product_id)
        .where(CartModel.user_id == user_id))
        
        result = (await self.session.execute(stmt)).mappings().fetchone()

        return UUID(result.id)


@dataclass(slots=True, kw_only=True)
class DeleteCartCustomGateway(PostgresGateway):
    async def __call__(self,  cart_product_id: UUID) -> bool:
        stmt_custom = delete(CustomsCartModel).where(CustomsCartModel.cart_product_id==cart_product_id)
        
        stmt_cart = delete(CartModel).where(CartModel.id==cart_product_id)
        try:

            (await self.session.execute(stmt_custom)).mappings().fetchall()
            (await self.session.execute(stmt_cart)).mappings().fetchall()
        except:
            return False
        return True
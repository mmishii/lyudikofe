from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.infra.postgres.tables import ProductsModel, CartModel, CustomsCartModel, ImagesModel, PricesModel
from src.usecase.carts.schemas import CartProductsSchema, CustomSchema
from sqlalchemy import select, func, literal, delete
from src.application.errors import NotFoundError
from uuid import UUID
from sqlalchemy.orm import aliased

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetCartGateway(PostgresGateway):
    async def __call__(self, user_id: UUID) -> list[CartProductsSchema]:
                
        IngredientModel = aliased(ProductsModel)
        ProductImageModel = aliased(ImagesModel)
        ProductPriceModel = aliased(PricesModel)
        IngredientPriceModel = aliased(PricesModel)

        stmt = (
            select(
                CartModel.id,
                CartModel.user_id,
                CartModel.quantity,

                func.json_build_object(
                    "id", ProductsModel.id,
                    "name", ProductsModel.name,
                    "is_available", ProductsModel.is_available,
                    "image_url", ProductImageModel.name,

                    "price", func.json_build_object(
                        "id", ProductPriceModel.id,
                        "price", ProductPriceModel.price,
                        "volume", ProductPriceModel.volume,
                        "created_at", ProductPriceModel.created_at,
                        "updated_at", ProductPriceModel.updated_at,
                    ),

                    "custom", func.json_agg(
                        func.json_build_object(
                            "id", CustomsCartModel.id,
                            "cart_product_id", CustomsCartModel.cart_product_id,
                            "ingredient_id", CustomsCartModel.ingredient_id,

                            "ingredient", func.json_build_object(
                                "id", IngredientModel.id,
                                "name", IngredientModel.name,
                                "is_available", IngredientModel.is_available,
                            ),

                            "price", func.json_build_object(
                                "id", IngredientPriceModel.id,
                                "price", IngredientPriceModel.price,
                                "volume", IngredientPriceModel.volume,
                                "created_at", IngredientPriceModel.created_at,
                                "updated_at", IngredientPriceModel.updated_at,
                            ),

                            "created_at", CustomsCartModel.created_at,
                            "updated_at", CustomsCartModel.updated_at,
                        )
                    ),

                    "created_at", ProductsModel.created_at,
                    "updated_at", ProductsModel.updated_at,
                ).label("products"),

                CartModel.created_at,
                CartModel.updated_at,
            )
            .select_from(CartModel)

            .join(
                ProductsModel,
                CartModel.product_id == ProductsModel.id
            )

            .join(
                ProductImageModel,
                ProductImageModel.product_id == ProductsModel.id
            )

            .join(
                ProductPriceModel,
                CartModel.price_id == ProductPriceModel.id
            )

            .outerjoin(
                CustomsCartModel,
                CustomsCartModel.cart_product_id == CartModel.id
            )

            .outerjoin(
                IngredientModel,
                CustomsCartModel.ingredient_id == IngredientModel.id
            )

            .outerjoin(
                IngredientPriceModel,
                CustomsCartModel.price_id == IngredientPriceModel.id
            )

            .where(CartModel.user_id == user_id)

            .group_by(
                CartModel.id,
                CartModel.user_id,
                CartModel.quantity,
                CartModel.created_at,
                CartModel.updated_at,

                ProductsModel.id,
                ProductsModel.name,
                ProductsModel.is_available,
                ProductsModel.created_at,
                ProductsModel.updated_at,

                ProductImageModel.name,

                ProductPriceModel.id,
                ProductPriceModel.price,
                ProductPriceModel.volume,
                ProductPriceModel.created_at,
                ProductPriceModel.updated_at,
            )
        )


        result = (await self.session.execute(stmt)).mappings().fetchall()
        if result is None:
            raise NotFoundError(table=ProductsModel)
        return [CartProductsSchema.model_validate(row) for row in result]




@dataclass(slots=True, kw_only=True)
class DeleteCartCustomGateway(PostgresGateway):
    async def __call__(self,  cart_product_id: UUID) -> bool:
        stmt_custom = delete(CustomsCartModel).where(CustomsCartModel.cart_product_id==cart_product_id)
        
        stmt_cart = delete(CartModel).where(CartModel.id==cart_product_id)
        try:

            await self.session.execute(stmt_custom)
            await self.session.execute(stmt_cart)
        except:
            return False
        return True
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.infra.postgres.tables import ProductsModel, FavoriteModel, ImagesModel, FavoriteCostumesModel, PricesModel
from src.usecase.favorites.schemas import GetFavoritesSchema, GetCustomFavoritesSchema
from sqlalchemy import select, func, literal, delete
from src.application.errors import NotFoundError
from uuid import UUID

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetFavoriteGateway(PostgresGateway):
    async def __call__(self, user_id: UUID) -> list[GetFavoritesSchema]:
        stmt = (select(
                FavoriteModel.id,
                FavoriteModel.user_id,
                func.json_build_object(
                        "id", ProductsModel.id,
                        "name", ProductsModel.name,
                        "is_available", ProductsModel.is_available,
                        "image_url", ImagesModel.name,
                        "price", PricesModel.price,
                        "volume", PricesModel.volume,
                    )
                .label("products"),
                FavoriteModel.created_at,
                FavoriteModel.updated_at)
            .join(FavoriteModel, FavoriteModel.product_id == ProductsModel.id)
            .join(ImagesModel, ImagesModel.product_id == ProductsModel.id)
            .join(PricesModel, PricesModel.id == FavoriteModel.price_id)
            .where(FavoriteModel.user_id == user_id)
        )


        result = (await self.session.execute(stmt)).mappings().fetchall()
        if result is None:
            raise NotFoundError(table=FavoriteModel)
        return [GetFavoritesSchema.model_validate(row) for row in result]
    


@dataclass(slots=True, kw_only=True)
class GetCustomFavoriteGateway(PostgresGateway):
    async def __call__(self, favorite_id: UUID) -> list[GetCustomFavoritesSchema]:
        stmt = (select(
                FavoriteCostumesModel.ingredient_id,
                (PricesModel.id).label("price_id"),
                PricesModel.price,
                PricesModel.volume,
                ProductsModel.name
            )
            .join(ProductsModel, ProductsModel.id == FavoriteCostumesModel.ingredient_id)
            .join(PricesModel, PricesModel.id == FavoriteCostumesModel.price_id)
            .where(FavoriteCostumesModel.favorite_id == favorite_id))

        result = (await self.session.execute(stmt)).mappings().fetchall()
        if result is None:
            raise NotFoundError(table=FavoriteCostumesModel)
        return [GetCustomFavoritesSchema.model_validate(row) for row in result]


@dataclass(slots=True, kw_only=True)
class GetFavoriteProductGateway(PostgresGateway):
    async def __call__(self, product_id: UUID, user_id: UUID) -> UUID:
        stmt = (select(
            FavoriteModel.id,
        )
        .where(FavoriteModel.product_id == product_id)
        .where(FavoriteModel.user_id == user_id))
        
        result = (await self.session.execute(stmt)).mappings().fetchone()

        return UUID(result.id)


@dataclass(slots=True, kw_only=True)
class DeleteFavoriteCustomGateway(PostgresGateway):
    async def __call__(self,  favorite_product_id: UUID) -> bool:
        stmt_custom = delete(FavoriteCostumesModel).where(FavoriteCostumesModel.favorite_id==favorite_product_id)
        
        stmt_cart = delete(FavoriteModel).where(FavoriteModel.id==favorite_product_id)
        try:

            (await self.session.execute(stmt_custom)).mappings().fetchall()
            (await self.session.execute(stmt_cart)).mappings().fetchall()
        except:
            return False
        return True      
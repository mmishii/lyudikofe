from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from src.application.schemas.favorites import FavoritesSchema, CreateFavoritesSchema
from src.application.schemas.custom_favorites import CreateCustomFavoritesSchema, CustomFavoritesSchema
from src.usecase.base import Usecase
from src.usecase.favorites.schemas import RequestCreateFavoritesSchema, ResponseCustomFavoritesSchema
from src.infra.postgres.tables import FavoriteModel, FavoriteCostumesModel
from src.infra.postgres.gateways.base import CreateReturningGate
from dataclasses import dataclass



@dataclass(slots=True, frozen=True, kw_only=True)
class CreateFavoriteUsecase(Usecase[RequestCreateFavoritesSchema, ResponseCustomFavoritesSchema]):
    session: AsyncSession
    user: AuthSchema
    create_favorite: CreateReturningGate[FavoriteModel, CreateFavoritesSchema, FavoritesSchema]
    create_custom_favorite: CreateReturningGate[FavoriteCostumesModel, CreateCustomFavoritesSchema, CustomFavoritesSchema]

    async def __call__(self, data: RequestCreateFavoritesSchema) -> ResponseCustomFavoritesSchema:
        async with self.session.begin():
            favorite = await self.create_favorite(
                CreateFavoritesSchema(
                    user_id=self.user.id,
                    price_id=data.price_id,
                    product_id=data.product_id
                )
            )
            customs = []
            for ingredient in data.custom:
                custom = await self.create_custom_favorite(
                    CreateCustomFavoritesSchema(
                        favorite_id=favorite.id,
                        ingredient_id=ingredient.ingredient_id,
                        price_id=ingredient.price_id,
                    )
                )
                customs.append(custom)
            
            return ResponseCustomFavoritesSchema(
                id=favorite.id,
                user_id=favorite.user_id,
                price_id=favorite.price_id,
                product_id=favorite.product_id,
                created_at=str(favorite.created_at),
                updated_at=str(favorite.updated_at),
                customs=customs
            )
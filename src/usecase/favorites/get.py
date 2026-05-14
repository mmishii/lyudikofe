from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from src.usecase.base import Usecase
from dataclasses import dataclass
from uuid import UUID
from src.infra.postgres.gateways.favorites import GetFavoriteGateway, GetCustomFavoriteGateway
from src.usecase.favorites.schemas import ResponseGetFavoritesSchema, GetFavorioteProductsSchema
from src.infra.minio.get import GetImg


@dataclass(slots=True, frozen=True, kw_only=True)
class GetFavoriteUsecase(Usecase[None, list[ResponseGetFavoritesSchema]]):
    session: AsyncSession
    user: AuthSchema
    get_favorites: GetFavoriteGateway
    get_custom_favorites: GetCustomFavoriteGateway
    get_img: GetImg

    async def __call__(self, data: None = None) -> list[ResponseGetFavoritesSchema]:
        async with self.session.begin():
            favorites = await self.get_favorites(self.user.id)

            favorites_with_customs = []
            for favorite in favorites:
                custom_favorites = await self.get_custom_favorites(favorite.id)
                favorite.products.image_url = await self.get_img(favorite.products.image_url)
                favorites_with_customs.append(
                    ResponseGetFavoritesSchema(
                        id=favorite.id,
                        user_id=favorite.user_id,
                        products=GetFavorioteProductsSchema(
                            id=favorite.products.id,
                            image_url=favorite.products.image_url,
                            name=favorite.products.name,
                            is_available=favorite.products.is_available,
                            price=favorite.products.price,
                            volume=favorite.products.volume
                        ),
                        customs=custom_favorites,
                        created_at=favorite.created_at,
                        updated_at=favorite.updated_at
                    )
                )

            return favorites_with_customs
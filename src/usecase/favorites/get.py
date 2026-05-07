from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from src.usecase.base import Usecase
from dataclasses import dataclass
from uuid import UUID
from src.infra.postgres.gateways.favorites import GetFavoriteGateway, GetCustomFavoriteGateway
from src.usecase.favorites.schemas import ResponseGetFavoritesSchema
from src.infra.minio.get import GetImg


@dataclass(slots=True, frozen=True, kw_only=True)
class GetFavoriteUsecase(Usecase[None, None]):
    session: AsyncSession
    user: AuthSchema
    get_favorites: GetFavoriteGateway
    get_custom_favorites: GetCustomFavoriteGateway
    get_img: GetImg

    async def __call__(self, data: None = None) -> None:
        async with self.session.begin():
            favorites = await self.get_favorites(self.user.id)

            favorites_with_customs = []
            for favorite in favorites:
                custom_favorites = await self.get_custom_favorites(favorite.id)
                favorite.image_url = await self.get_img(favorite.image_url)
                favorites_with_customs.append(
                    ResponseGetFavoritesSchema(
                        id=favorite.id,
                        user_id=favorite.user_id,
                        product_id=favorite.product_id,
                        name=favorite.name,
                        image_url=favorite.image_url,
                        customs=custom_favorites,
                        created_at=favorite.created_at,
                        updated_at=favorite.updated_at
                    )
                )

            return favorites_with_customs
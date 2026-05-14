from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.products import GetProductByIdGateway
from src.usecase.products.schemas import ResponseOneProduct, RespopnseMacrosSchema
from src.infra.postgres.gateways.images import GetImageNameGateway
from dataclasses import dataclass
from src.infra.minio.get import GetImg


@dataclass(slots=True, frozen=True, kw_only=True)
class GetProductByIdUsecase(Usecase[UUID, ResponseOneProduct]):
    session: AsyncSession
    get_drink: GetProductByIdGateway
    get_img_url: GetImageNameGateway
    get_img: GetImg

    async def __call__(self, data_id: UUID) -> ResponseOneProduct:
        async with self.session.begin():
            drink = await self.get_drink(data_id=data_id)
            drink.image_url = await self.get_img_url(drink.id)
            drink.image_url = await self.get_img(drink.image_url)
            price = []
            for i in drink.prices:
                price.append(RespopnseMacrosSchema(
                    price=i.price,
                    price_id=i.price_id,
                    volume=i.volume,
                    unit_kkal=drink.unit_kkal * i.volume / 100,
                    unit_fats=drink.unit_fats * i.volume / 100,
                    unit_carbs=drink.unit_carbs * i.volume / 100,
                    unit_proteins=drink.unit_proteins * i.volume / 100,
                ))
            return ResponseOneProduct(
                id=drink.id,
                name = drink.name,
                description=drink.description,
                ingredients=drink.ingredients,
                prices=price,
                is_available=drink.is_available,
                category=drink.category,
                season=drink.season,
                image_url=drink.image_url,
                created_at=drink.created_at,
                updated_at=drink.updated_at
            )


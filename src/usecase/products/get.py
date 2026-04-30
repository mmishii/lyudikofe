from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.products import GetProductsGateway
from src.usecase.products.schemas import ResponseProducts
from src.infra.postgres.gateways.images import GetImageNameGateway
from src.application.schemas.common import ResponsePaginationSchema, RequestPaginationSchema
from src.application.services.pagination import Pagination
from dataclasses import dataclass
from src.infra.minio.get import GetImg

@dataclass(slots=True, frozen=True, kw_only=True)
class GetDrinksUsecase(Usecase[RequestPaginationSchema, ResponsePaginationSchema[ResponseProducts]]):
    session: AsyncSession
    get_products: GetProductsGateway
    pagination: Pagination[ResponseProducts]
    get_img_url: GetImageNameGateway
    get_img: GetImg
    
    async def __call__(self, data: RequestPaginationSchema) -> ResponsePaginationSchema[ResponseProducts]:
        async with self.session.begin():
            products = await self.get_products(category=data.category)
            for i in range(len(products)):
                products[i].image_url = await self.get_img_url(products[i].id)
                products[i].image_url = await self.get_img(products[i].image_url)
            return self.pagination(
                items=products,
            limit=data.limit,
            offset=data.offset,
            schema_class=ResponseProducts)
            
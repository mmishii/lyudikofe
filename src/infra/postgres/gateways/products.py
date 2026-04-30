from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.infra.postgres.tables import ProductsModel, MacrosModel, PricesModel, ImagesModel
from src.usecase.products.schemas import ResponseProducts, ResponseProduct
from sqlalchemy import select, func, literal
from src.application.errors import NotFoundError
from uuid import UUID

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetProductsGateway(PostgresGateway):
    async def __call__(self, category: str) -> list[ResponseProducts]:
        stmt = (select(
                ProductsModel.id,
                ProductsModel.name,
                ProductsModel.description,
                ProductsModel.ingredients,
                ProductsModel.is_available,
                ProductsModel.category,
                ProductsModel.season,
                func.concat(
                    PricesModel.price,
                    PricesModel.volume
                ).label('price'),
                ProductsModel.created_at,
                ProductsModel.updated_at
            )
            .join(PricesModel, PricesModel.product_id == ProductsModel.id)
            .where(ProductsModel.category==category))


        result = (await self.session.execute(stmt)).mappings().fetchall()
        if result is None:
            raise NotFoundError(table=ProductsModel)
        return [ResponseProducts.model_validate(row) for row in result]
    

@dataclass(slots=True, kw_only=True)
class GetProductByIdGateway(PostgresGateway):
    async def __call__(self, data_id: UUID) -> ResponseProduct:
        stmt = (select(
                ProductsModel.id,
                ProductsModel.name,
                ProductsModel.description,
                ProductsModel.ingredients,
                ProductsModel.is_available,
                ProductsModel.category,
                ProductsModel.season,
                MacrosModel.unit_kkal,
                MacrosModel.unit_fats,
                MacrosModel.unit_carbs,
                MacrosModel.unit_proteins,
                func.concat(
                    PricesModel.price,
                    PricesModel.volume
                ).label('price'),
                ProductsModel.created_at,
                ProductsModel.updated_at
            )
            .join(PricesModel, PricesModel.product_id == ProductsModel.id)
            .join(MacrosModel, MacrosModel.id == ProductsModel.macros_id)
                .where(ProductsModel.id == data_id))


        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise NotFoundError(table=ProductsModel)
        return ResponseProduct.model_validate(result)

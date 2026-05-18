from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.infra.postgres.tables import ProductsModel, MacrosModel, PricesModel, ImagesModel
from src.usecase.products.schemas import ResponseProducts, ResponseProduct
from sqlalchemy import select, func, literal
from src.application.errors import NotFoundError
from uuid import UUID
from loguru import logger

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetProductsGateway(PostgresGateway):
    async def __call__(self, category: str, season:str | None = None) -> list[ResponseProducts]:
        stmt = (select(
                ProductsModel.id,
                ProductsModel.name,
                ProductsModel.description,
                ProductsModel.ingredients,
                ProductsModel.is_available,
                ProductsModel.category,
                ProductsModel.season,
                (ImagesModel.name).label("image_url"),
                 func.coalesce(
                    func.json_agg(
                        func.json_build_object(
                            "price_id", PricesModel.id,
                            'price', PricesModel.price,
                            'volume', PricesModel.volume
                        )
                    ),
                    func.json_build_array()
                ).label('prices'),
                ProductsModel.created_at,
                ProductsModel.updated_at
            )
            .join(PricesModel, PricesModel.product_id == ProductsModel.id)
            .join(ImagesModel, ImagesModel.product_id == ProductsModel.id)

            .where(ProductsModel.category==category)
            .group_by(
                ProductsModel.id,
                ProductsModel.name,
                ProductsModel.description,
                ProductsModel.ingredients,
                ProductsModel.is_available,
                ProductsModel.category,
                ProductsModel.season,
                ImagesModel.name,
                ProductsModel.created_at,
                ProductsModel.updated_at
            ))

        if season is not None and season != "null" and season != "":
            stmt = stmt.where(ProductsModel.season == season)
        result = (await self.session.execute(stmt)).mappings().fetchall()
        logger.info(result)
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
                (MacrosModel.id).label("macros_id"),
                MacrosModel.unit_kkal,
                MacrosModel.unit_fats,
                MacrosModel.unit_carbs,
                MacrosModel.unit_proteins,
                (ImagesModel.name).label("image_url"),
                func.coalesce(
                    func.json_agg(
                        func.json_build_object(
                            'price_id', PricesModel.id,
                            'price', PricesModel.price,
                            'volume', PricesModel.volume
                        )
                    ),
                    func.json_build_array()  # пустой список, если нет цен
                ).label('prices'),
                ProductsModel.created_at,
                ProductsModel.updated_at
            )
            .join(PricesModel, PricesModel.product_id == ProductsModel.id)
            .join(MacrosModel, MacrosModel.id == ProductsModel.macros_id)
            .join(ImagesModel, ImagesModel.product_id == ProductsModel.id)
                .where(ProductsModel.id == data_id)
            .group_by(
                ProductsModel.id,
                ProductsModel.name,
                ProductsModel.description,
                ProductsModel.ingredients,
                ProductsModel.is_available,
                ProductsModel.category,
                ProductsModel.season,
                MacrosModel.id,
                MacrosModel.unit_kkal,
                MacrosModel.unit_fats,
                MacrosModel.unit_carbs,
                MacrosModel.unit_proteins,
                ImagesModel.name,
                ProductsModel.created_at,
                ProductsModel.updated_at
            ))


        result = (await self.session.execute(stmt)).mappings().fetchone()
        logger.info(result)
        if result is None:
            raise NotFoundError(table=ProductsModel)
        return ResponseProduct.model_validate(result)

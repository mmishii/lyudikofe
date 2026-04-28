from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.usecase.food.schemas import ResponseAllFood, RequestFood,ApiPriceSchema
from src.application.schemas.macros import CreateMacrosSchema, MacrosSchema
from src.application.schemas.food import FoodSchema, CreateFoodSchema
from src.application.schemas.prices import CreatePriceSchema
from src.application.schemas.images import CreateImageSchema, ImageSchema
from src.infra.postgres.tables import MacrosModel, FoodModel, PricesModel, ImagesModel
from src.infra.minio.get import GetImg
from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateFoodUsecase(Usecase[RequestFood, ResponseAllFood]):
    session: AsyncSession
    create_macros: CreateReturningGate[MacrosModel, CreateMacrosSchema, MacrosSchema]
    create_food: CreateReturningGate[FoodModel, CreateFoodSchema, FoodSchema]
    create_price: CreateReturningGate[PricesModel, CreatePriceSchema, ApiPriceSchema]
    create_image: CreateReturningGate[ImagesModel, CreateImageSchema, ImageSchema]
    get_img: GetImg

    async def __call__(self, data: RequestFood) -> ResponseAllFood:
        async with self.session.begin():
            macros = await self.create_macros(CreateMacrosSchema(
                unit_kkal=data.unit_kkal,
                unit_proteins=data.unit_proteins,
                unit_carbs=data.unit_carbs,
                unit_fats=data.unit_fats
            ))

            food = await self.create_food(CreateFoodSchema(
                name=data.name,
                description=data.description,
                is_available=data.is_available,
                category=data.category,
                macros_id=macros.id,
            ))
            image = await self.create_image(CreateImageSchema(
                name=data.image_name,
                drink_id=food.id,
            ))
            image_url = await self.get_img(image.name)
            prices = []
            for price in data.prices:
                result = await self.create_price(CreatePriceSchema(
                    food_id=food.id,
                    price=price.price,
                    volume=price.volume,
                ))
                prices.append(result)

        return ResponseAllFood(
            id=food.id,
            name=food.name,
            description=food.description,
            is_available=food.is_available,
            prices=prices,
            image_url=image_url,
            category=food.category,
            macros_id=food.macros_id,
            unit_kkal=macros.unit_kkal,
            unit_proteins=macros.unit_proteins,
            unit_carbs=macros.unit_carbs,
            unit_fats=macros.unit_fats,
            created_at=food.created_at,
            updated_at=food.updated_at,
        )


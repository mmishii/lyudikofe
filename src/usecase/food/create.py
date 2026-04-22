from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.usecase.food.schemas import ResponseFood, RequestFood,ApiPriceSchema
from src.application.schemas.macros import CreateMacrosSchema, MacrosSchema
from src.application.schemas.food import FoodSchema, CreateFoodSchema
from src.application.schemas.prices import CreatePriceSchema
from src.infra.postgres.tables import MacrosModel, FoodModel, PricesModel
from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateFoodUsecase(Usecase[RequestFood, ResponseFood]):
    session: AsyncSession
    create_macros: CreateReturningGate[MacrosModel, CreateMacrosSchema, MacrosSchema]
    create_food: CreateReturningGate[FoodModel, CreateFoodSchema, FoodSchema]
    create_price: CreateReturningGate[PricesModel, CreatePriceSchema, ApiPriceSchema]

    async def __call__(self, data: RequestFood) -> ResponseFood:
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
            prices = []
            for price in data.prices:
                result = await self.create_price(CreatePriceSchema(
                    food_id=food.id,
                    price=price.price,
                    volume=price.volume,
                ))
                prices.append(result)

        return ResponseFood(
            id=food.id,
            name=food.name,
            description=food.description,
            is_available=food.is_available,
            prices=prices,
            category=food.category,
            macros_id=food.macros_id,
            unit_kkal=macros.unit_kkal,
            unit_proteins=macros.unit_proteins,
            unit_carbs=macros.unit_carbs,
            unit_fats=macros.unit_fats,
            created_at=food.created_at,
            updated_at=food.updated_at,
        )


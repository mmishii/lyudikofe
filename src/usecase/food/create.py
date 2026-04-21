from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.usecase.drinks.schemas import RequestDrink, ResponseDrink
from src.application.schemas.macros import CreateMacrosSchema, MacrosSchema
from src.application.schemas.drinks import CreateDrinkSchema, DrinkSchema
from src.infra.postgres.tables import MacrosModel, DrinksModel
from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateDrinkUsecase(Usecase[RequestDrink, ResponseDrink]):
    session: AsyncSession
    create_macros: CreateReturningGate[MacrosModel, CreateMacrosSchema, MacrosSchema]
    create_drink: CreateReturningGate[DrinksModel, CreateDrinkSchema, DrinkSchema]

    async def __call__(self, data: RequestDrink) -> ResponseDrink:
        async with self.session.begin():
            macros = await self.create_macros(CreateMacrosSchema(
                unit_kkal=data.unit_kkal,
                unit_proteins=data.unit_proteins,
                unit_carbs=data.unit_carbs,
                unit_fats=data.unit_fats
            ))

            drink = await self.create_drink(CreateDrinkSchema(
                name=data.name,
                description=data.description,
                price=data.price,
                is_available=data.is_available,
                category=data.category,
                season=data.season,
                macros_id=macros.id,
                volume=data.volume
            ))

        return ResponseDrink(
            id=drink.id,
            name=drink.name,
            description=drink.description,
            price=drink.price,
            is_available=drink.is_available,
            category=drink.category,
            season=drink.season,
            macros_id=drink.macros_id,
            volume=drink.volume,
            unit_kkal=macros.unit_kkal,
            unit_proteins=macros.unit_proteins,
            unit_carbs=macros.unit_carbs,
            unit_fats=macros.unit_fats,
            created_at=drink.created_at,
            updated_at=drink.updated_at,
        )


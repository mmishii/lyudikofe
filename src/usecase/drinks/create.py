from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.usecase.drinks.schemas import RequestDrink, ResponseAllDrink, ApiPriceSchema
from src.application.schemas.macros import CreateMacrosSchema, MacrosSchema
from src.application.schemas.drinks import CreateDrinkSchema, DrinkSchema
from src.application.schemas.prices import CreatePriceSchema
from src.application.schemas.images import CreateImageSchema, ImageSchema
from src.infra.postgres.tables import MacrosModel, DrinksModel, PricesModel, ImagesModel
from src.infra.minio.get import GetImg
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateDrinkUsecase(Usecase[RequestDrink, ResponseAllDrink]):
    session: AsyncSession
    create_macros: CreateReturningGate[MacrosModel, CreateMacrosSchema, MacrosSchema]
    create_drink: CreateReturningGate[DrinksModel, CreateDrinkSchema, DrinkSchema]
    create_price: CreateReturningGate[PricesModel, CreatePriceSchema, ApiPriceSchema]
    create_image: CreateReturningGate[ImagesModel, CreateImageSchema, ImageSchema]
    get_img: GetImg

    async def __call__(self, data: RequestDrink) -> ResponseAllDrink:
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
                is_available=data.is_available,
                category=data.category,
                season=data.season,
                macros_id=macros.id,
            ))
            image = await self.create_image(CreateImageSchema(
                name=data.image_name,
                drink_id=drink.id,
            ))
            image_url = await self.get_img(image.name)
            prices = []
            for price in data.prices:
                result = await self.create_price(CreatePriceSchema(
                    drink_id=drink.id,
                    price=price.price,
                    volume=price.volume,
                ))
                prices.append(result)


        return ResponseAllDrink(
            id=drink.id,
            name=drink.name,
            description=drink.description,
            prices=prices,
            is_available=drink.is_available,
            category=drink.category,
            image_url=image_url,
            season=drink.season,
            macros_id=drink.macros_id,
            unit_kkal=macros.unit_kkal,
            unit_proteins=macros.unit_proteins,
            unit_carbs=macros.unit_carbs,
            unit_fats=macros.unit_fats,
            created_at=drink.created_at,
            updated_at=drink.updated_at,
        )
            
        
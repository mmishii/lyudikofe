from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from uuid import UUID
from fastapi import status
from src.application.schemas.common import RequestPaginationSchema, ResponsePaginationSchema
from src.usecase.drinks.schemas import ResponseDrink, ResponseAllDrink, RequestDrink, ResponseOneDrink
from src.usecase.drinks.get import GetDrinksUsecase
from src.usecase.drinks.get_one import GetDrinkByIdUsecase
from src.usecase.drinks.create import CreateDrinkUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseAllDrink)
async def create_drinks(
    usecase: FromDishka[CreateDrinkUsecase],
    drink: RequestDrink) -> ResponseAllDrink:
    return await usecase(drink)



@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ResponsePaginationSchema[ResponseDrink])
async def get_drinks(
    usecase: FromDishka[GetDrinksUsecase],
    pagination: RequestPaginationSchema=Query(...)) -> ResponsePaginationSchema[ResponseDrink]:
    return await usecase(pagination)

@ROUTER.get('/by-id', status_code=status.HTTP_200_OK, response_model=ResponseOneDrink)
async def get_drinks(
    usecase: FromDishka[GetDrinkByIdUsecase],
    data_id: UUID=Query(...)) -> ResponseOneDrink:
    return await usecase(data_id)


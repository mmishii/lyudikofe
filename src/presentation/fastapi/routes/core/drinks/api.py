from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from fastapi import status
from src.application.schemas.common import PaginationSchema, ResponsePaginationSchema
from src.usecase.drinks.schemas import ResponseDrink, RequestDrink
from src.usecase.drinks.get import GetDrinksUsecase
from src.usecase.drinks.create import CreateDrinkUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseDrink)
async def create_drinks(
    usecase: FromDishka[CreateDrinkUsecase],
    drink: RequestDrink) -> ResponseDrink:
    return await usecase(drink)



@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ResponsePaginationSchema[ResponseDrink])
async def get_drinks(
    usecase: FromDishka[GetDrinksUsecase],
    pagination: PaginationSchema=Query(...)) -> ResponsePaginationSchema[ResponseDrink]:
    return await usecase(pagination)

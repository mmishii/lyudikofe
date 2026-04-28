from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from fastapi import status
from src.application.schemas.common import RequestPaginationSchema, ResponsePaginationSchema
from src.usecase.food.schemas import RequestFood, ResponseFood, ResponseAllFood
from src.usecase.food.create import CreateFoodUsecase
from src.usecase.food.get import GetFoodUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseAllFood)
async def create_drinks(
    usecase: FromDishka[CreateFoodUsecase],
    food: RequestFood) -> ResponseAllFood:
    return await usecase(food)

@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ResponsePaginationSchema[ResponseFood])
async def get_ingredients(
    usecase: FromDishka[GetFoodUsecase],
    pagination: RequestPaginationSchema=Query(...)) -> ResponsePaginationSchema[ResponseFood]:
    return await usecase(pagination)


from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from uuid import UUID
from fastapi import status
from src.application.schemas.common import RequestPaginationSchema, ResponsePaginationSchema
from src.usecase.food.schemas import RequestFood, ResponseFood, ResponseAllFood
from src.usecase.food.get_one import GetFoodByIdUsecase
from src.usecase.food.create import CreateFoodUsecase
from src.usecase.food.get import GetFoodUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseAllFood)
async def create_food(
    usecase: FromDishka[CreateFoodUsecase],
    food: RequestFood) -> ResponseAllFood:
    return await usecase(food)

@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ResponsePaginationSchema[ResponseFood])
async def get_foods(
    usecase: FromDishka[GetFoodUsecase],
    pagination: RequestPaginationSchema=Query(...)) -> ResponsePaginationSchema[ResponseFood]:
    return await usecase(pagination)

@ROUTER.get('/by-id', status_code=status.HTTP_200_OK, response_model=ResponseAllFood)
async def get_food_by_id(
    usecase: FromDishka[GetFoodByIdUsecase],
    data_id: UUID=Query(...)) -> ResponseAllFood:
    return await usecase(data_id)



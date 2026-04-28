from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import APIRouter, Query
from fastapi import status
from src.application.schemas.common import RequestPaginationSchema, ResponsePaginationSchema
from src.usecase.ingredients.schemas import ResponseIngredients
from src.usecase.ingredients.get import GetIngredientsUsecase
ROUTER = APIRouter(route_class=DishkaRoute)


@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ResponsePaginationSchema[ResponseIngredients])
async def get_ingredients(
    usecase: FromDishka[GetIngredientsUsecase],
    pagination: RequestPaginationSchema=Query(...)) -> ResponsePaginationSchema[ResponseIngredients]:
    return await usecase(pagination)


from uuid import UUID
from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import APIRouter, Query
from fastapi import status
from src.application.schemas.common import RequestPaginationSchema, ResponsePaginationSchema
from src.usecase.ingredients.schemas import ResponseIngredients, ResponseAllIngredients
from src.usecase.ingredients.get import GetIngredientsUsecase
from src.usecase.ingredients.get_one import GetIngredientByIdUsecase
ROUTER = APIRouter(route_class=DishkaRoute)


@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ResponsePaginationSchema[ResponseIngredients])
async def get_ingredients(
    usecase: FromDishka[GetIngredientsUsecase],
    pagination: RequestPaginationSchema=Query(...)) -> ResponsePaginationSchema[ResponseIngredients]:
    return await usecase(pagination)


@ROUTER.get('/by-id', status_code=status.HTTP_200_OK, response_model=ResponseAllIngredients)
async def get_ingredient_by_id(
    usecase: FromDishka[GetIngredientByIdUsecase],
    data_id: UUID = Query(...)) -> ResponseAllIngredients:
    return await usecase(data_id=data_id)

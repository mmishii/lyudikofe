from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from src.usecase.favorites.create import CreateFavoriteUsecase
from src.usecase.favorites.schemas import RequestCreateFavoritesSchema, ResponseCustomFavoritesSchema
from src.usecase.favorites.get import GetFavoriteUsecase
from src.usecase.favorites.schemas import ResponseGetFavoritesSchema


ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=200, response_model=ResponseCustomFavoritesSchema)
async def create_favorite(
    usecase: FromDishka[CreateFavoriteUsecase],
    data: RequestCreateFavoritesSchema) -> ResponseCustomFavoritesSchema:
    return await usecase(data)

@ROUTER.get('', status_code=200, response_model=ResponseGetFavoritesSchema)
async def get_favorites(
    usecase: FromDishka[GetFavoriteUsecase]) -> ResponseGetFavoritesSchema:
    return await usecase()
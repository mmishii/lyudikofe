from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from uuid import UUID
from src.usecase.favorites.create import CreateFavoriteUsecase
from src.usecase.favorites.schemas import RequestCreateFavoritesSchema, ResponseCustomFavoritesSchema
from src.usecase.favorites.get import GetFavoriteUsecase
from src.usecase.favorites.schemas import ResponseGetFavoritesSchema
from src.usecase.favorites.delete import DeleteFavoritesUsecase


ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=200, response_model=ResponseCustomFavoritesSchema)
async def create_favorite(
    usecase: FromDishka[CreateFavoriteUsecase],
    data: RequestCreateFavoritesSchema) -> ResponseCustomFavoritesSchema:
    return await usecase(data)

@ROUTER.get('', status_code=200, response_model=list[ResponseGetFavoritesSchema])
async def get_favorites(
    usecase: FromDishka[GetFavoriteUsecase]) -> list[ResponseGetFavoritesSchema]:
    return await usecase()

@ROUTER.delete('', status_code=200, response_model=bool)
async def delete_favorite(
    usecase: FromDishka[DeleteFavoritesUsecase],
    product_id: UUID) -> bool:
    return await usecase(product_id=product_id)
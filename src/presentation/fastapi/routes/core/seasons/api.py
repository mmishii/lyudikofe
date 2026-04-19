from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.string import CreateStringSchema, StringSchema
from src.usecase.seazons.create import CreateSeasonUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=StringSchema)
async def create_season(
    usecase: FromDishka[CreateSeasonUsecase],
    data: CreateStringSchema) -> StringSchema:
    return await usecase(data)

from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.string import CreateStringSchema, StringSchema
from src.usecase.categories.create import CreateCategoryUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=StringSchema)
async def create_category(
    usecase: FromDishka[CreateCategoryUsecase],
    data: CreateStringSchema) -> StringSchema:
    return await usecase(data)

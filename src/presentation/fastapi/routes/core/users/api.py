from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.users import CreateUserSchema, UserSchemas
from src.usecase.users.create import CreateUserUsecase
from src.usecase.users.get import GetUserUsecase

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=UserSchemas)
async def create_user(
    usecase: FromDishka[CreateUserUsecase],
    user: CreateUserSchema) -> UserSchemas:
    return await usecase(user)


@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=UserSchemas)
async def get_user(
    usecase: FromDishka[GetUserUsecase],) -> UserSchemas:
    return await usecase()

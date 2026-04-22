from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.usecase.food.schemas import RequestFood, ResponseFood
from src.usecase.food.create import CreateFoodUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseFood)
async def create_drinks(
    usecase: FromDishka[CreateFoodUsecase],
    drink: RequestFood) -> ResponseFood:
    return await usecase(drink)


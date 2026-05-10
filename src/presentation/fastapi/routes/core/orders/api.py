
from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status

from src.usecase.orders.schemas import RequestOrderSchema, ResponseOrderSchema
from src.usecase.orders.create import CreateOrderUsecase


ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseOrderSchema)
async def create_order(
    usecase: FromDishka[CreateOrderUsecase],
    order_data: RequestOrderSchema) -> ResponseOrderSchema:
    return await usecase(order_data)
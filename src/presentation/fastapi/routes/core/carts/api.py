from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status

from src.usecase.carts.create import CreateCartUsecase
from src.usecase.carts.schemas import RequestCartProducts, ResponseCartProducts, CartProductsSchema
from src.usecase.carts.get import GetCartUsecase
from src.usecase.carts.schemas import ResponseCartProductsSchema
from src.usecase.carts.delete import DeleteCartUsecase

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseCartProducts|None)
async def create_cart(
    usecase: FromDishka[CreateCartUsecase],
    cart_products: RequestCartProducts) -> ResponseCartProducts|None:
    return await usecase(cart_products)

@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=list[CartProductsSchema])
async def get_cart(
    usecase: FromDishka[GetCartUsecase],
    ) -> list[CartProductsSchema]:
    return await usecase()

@ROUTER.delete('', status_code=status.HTTP_200_OK, response_model=bool)
async def delete_cart(
    usecase: FromDishka[DeleteCartUsecase],
    cart_product_id: UUID
    ) -> bool:
    return await usecase(cart_product_id=cart_product_id)
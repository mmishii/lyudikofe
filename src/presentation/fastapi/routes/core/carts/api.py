from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status

from src.usecase.carts.create import CreateCartUsecase
from src.usecase.carts.schemas import RequestCartProducts, ResponseCartProducts
from src.usecase.carts.get import GetCartUsecase
from src.usecase.carts.schemas import ResponseCartProductsSchema
from src.usecase.carts.delete import DeleteCartUsecase

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseCartProducts)
async def create_cart(
    usecase: FromDishka[CreateCartUsecase],
    cart_products: RequestCartProducts) -> ResponseCartProducts:
    return await usecase(cart_products)

@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ResponseCartProductsSchema)
async def get_cart(
    usecase: FromDishka[GetCartUsecase],
    ) -> ResponseCartProductsSchema:
    return await usecase()

@ROUTER.delete('', status_code=status.HTTP_200_OK, response_model=bool)
async def delete_cart(
    usecase: FromDishka[DeleteCartUsecase],
    product_id: UUID
    ) -> bool:
    return await usecase(product_id=product_id)
from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from uuid import UUID
from fastapi import status
from src.application.schemas.common import RequestPaginationSchema, ResponsePaginationSchema
from src.usecase.products.schemas import ResponseProduct, RequestProduct, ResponseProducts, ResponseOneProduct
from src.usecase.products.get import GetProductUsecase
from src.usecase.products.get_one import GetProductByIdUsecase
from src.usecase.products.create import CreateProductUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseProduct)
async def create_drinks(
    usecase: FromDishka[CreateProductUsecase],
    product: RequestProduct) -> ResponseProduct:
    return await usecase(product)



@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ResponsePaginationSchema[ResponseProducts])
async def get_drinks(
    usecase: FromDishka[GetProductUsecase],
    pagination: RequestPaginationSchema=Query(...)) -> ResponsePaginationSchema[ResponseProducts]:
    return await usecase(pagination)

@ROUTER.get('/by-id', status_code=status.HTTP_200_OK, response_model=ResponseOneProduct)
async def get_drinks(
    usecase: FromDishka[GetProductByIdUsecase],
    data_id: UUID=Query(...)) -> ResponseOneProduct:
    return await usecase(data_id)


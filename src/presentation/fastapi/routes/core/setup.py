from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.fastapi.routes.core.users.api import ROUTER as USERS_ROUTER
from src.presentation.fastapi.routes.core.products.api import ROUTER as PRODUCTS_ROUTER
from src.presentation.fastapi.routes.core.categories.api import ROUTER as CATEGORIES_ROUTER
from src.presentation.fastapi.routes.core.seasons.api import ROUTER as SEASONS_ROUTER
from src.presentation.fastapi.routes.core.carts.api import ROUTER as CARTS_ROUTER

def setup_core_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)

    router.include_router(prefix='/users', router=USERS_ROUTER)
    router.include_router(prefix='/products', router=PRODUCTS_ROUTER)
    router.include_router(prefix='/categories', router=CATEGORIES_ROUTER)
    router.include_router(prefix='/seasons', router=SEASONS_ROUTER)
    router.include_router(prefix='/carts', router=CARTS_ROUTER)

    return router

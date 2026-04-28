from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.fastapi.routes.core.drinks.api import ROUTER as DRINKS_ROUTER
from src.presentation.fastapi.routes.core.categories.api import ROUTER as CATEGORIES_ROUTER
from src.presentation.fastapi.routes.core.seasons.api import ROUTER as SEASONS_ROUTER
from src.presentation.fastapi.routes.core.food.api import ROUTER as FOOD_ROUTER
from src.presentation.fastapi.routes.core.ingredients.api import ROUTER as INGREDIENTS_ROUTER

def setup_core_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)

    router.include_router(prefix='/drinks', router=DRINKS_ROUTER)
    router.include_router(prefix='/categories', router=CATEGORIES_ROUTER)
    router.include_router(prefix='/seasons', router=SEASONS_ROUTER)
    router.include_router(prefix='/food', router=FOOD_ROUTER)
    router.include_router(prefix='/ingredients', router=INGREDIENTS_ROUTER)

    return router

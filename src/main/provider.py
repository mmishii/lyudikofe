from dishka import Provider
from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka import provide_all
from fastapi import Request

from src.application.services.pagination import Pagination
from src.config import Config
from src.config import ApiConfig
from src.config import DatabaseConfig

from src.usecase.drinks.get import GetDrinksUsecase
from src.usecase.drinks.create import CreateDrinkUsecase
from src.usecase.drinks.get_one import GetDrinkByIdUsecase
from src.usecase.food.create import CreateFoodUsecase
from src.usecase.food.get import GetFoodUsecase
from src.usecase.categories.create import CreateCategoryUsecase
from src.usecase.seazons.create import CreateSeasonUsecase
from src.infra.minio.get import GetImg
from src.usecase.ingredients.get import GetIngredientsUsecase

class MainProvider(Provider):
    scope = Scope.REQUEST

    _provide_config = from_context(provides=Config, scope=Scope.APP) 

    @provide(scope=Scope.APP)
    async def _get_api_config(self, config: Config) -> ApiConfig:
        return config.api
    
    @provide(scope=Scope.APP)
    async def _get_database_config(self, config: Config) -> DatabaseConfig:
        return config.database

    _request = from_context(provides=Request, scope=Scope.REQUEST)

    _get_usecases = provide_all(
        Pagination,
        GetDrinksUsecase,
        CreateDrinkUsecase,
        CreateCategoryUsecase,
        CreateSeasonUsecase,
        CreateFoodUsecase,
        GetImg,
        GetFoodUsecase,
        GetIngredientsUsecase,
        GetDrinkByIdUsecase,
    )


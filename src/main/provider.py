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

from src.usecase.users.create import CreateUserUsecase
from src.usecase.users.get import GetUserUsecase
from src.usecase.products.get import GetProductUsecase
from src.usecase.products.create import CreateProductUsecase
from src.usecase.products.get_one import GetProductByIdUsecase
from src.usecase.categories.create import CreateCategoryUsecase
from src.usecase.seazons.create import CreateSeasonUsecase
from src.infra.minio.get import GetImg
from src.usecase.carts.create import CreateCartUsecase
from src.usecase.carts.get import GetCartUsecase
from src.usecase.carts.delete import DeleteCartUsecase
from src.usecase.favorites.create import CreateFavoriteUsecase
from src.usecase.favorites.get import GetFavoriteUsecase

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
        CreateUserUsecase,
        GetUserUsecase,
        Pagination,
        GetProductUsecase,
        CreateProductUsecase,
        CreateCategoryUsecase,
        CreateSeasonUsecase,
        GetImg,
        GetProductByIdUsecase,
        CreateCartUsecase,
        GetCartUsecase,
        DeleteCartUsecase,
        CreateFavoriteUsecase,
        GetFavoriteUsecase,
    )


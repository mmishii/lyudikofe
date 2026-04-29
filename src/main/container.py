from dishka import make_async_container
from src.main.provider import MainProvider
from src.infra.postgres.provider import PostgresProvider
from src.config import Config
from src.main.config import config
from src.infra.minio.provider import MinioProvider
from src.infra.auth.provider import AuthProvider

container = make_async_container(
    MainProvider(),
    PostgresProvider(),
    MinioProvider(),
    AuthProvider(),
    context={
        Config: config
    }
)
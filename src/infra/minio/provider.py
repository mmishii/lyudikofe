from dishka import Provider
from dishka import Scope
from dishka import provide

from src.infra.minio.get import GetImg

class MinioProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    async def _get_img(self, ) -> GetImg:
        return GetImg()

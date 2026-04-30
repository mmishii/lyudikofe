from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from uuid import UUID
from src.infra.postgres.tables import ImagesModel
from sqlalchemy import select
from src.application.errors import NotFoundError


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetImageNameGateway(PostgresGateway):
    async def __call__(self, product_id: UUID) -> str:
        stmt = select(ImagesModel.name,
                      ImagesModel.product_id).where(
                        ImagesModel.product_id == product_id,
                    )
        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise NotFoundError(table=ImagesModel)
        return result.name

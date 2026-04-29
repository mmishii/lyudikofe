from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.base import GetByIdGate
from src.application.schemas.users import UserSchemas
from src.infra.postgres.tables import UsersModel
from src.application.schemas.auth import AuthSchema
from dataclasses import dataclass
from loguru import logger

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserUsecase(Usecase[None, UserSchemas]):
    session: AsyncSession
    get_user: GetByIdGate[UsersModel, UUID, UserSchemas]
    auth: AuthSchema

    async def __call__(self, data: None = None) -> UserSchemas:
        async with self.session.begin():
            logger.info(f"auth: {self.auth.id}")
            return await self.get_user(self.auth.id)

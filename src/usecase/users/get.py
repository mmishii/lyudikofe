from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.base import GetByIdGate
from src.application.schemas.users import UserSchemas
from src.infra.postgres.tables import UsersModel
from src.application.schemas.auth import AuthSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserUsecase(Usecase[None, UserSchemas]):
    session: AsyncSession
    get_user: GetByIdGate[UsersModel, UUID, UserSchemas]
    auth: AuthSchema

    async def __call__(self, data: None) -> UserSchemas:
        async with self.session.begin():
            return await self.get_user(self.auth.id)

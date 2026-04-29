from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.application.schemas.users import CreateUserSchema, UserSchemas
from src.infra.postgres.tables import UsersModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, UserSchemas]):
    session: AsyncSession
    create_user: CreateReturningGate[UsersModel, CreateUserSchema, UserSchemas]
    
    async def __call__(self, data: CreateUserSchema) -> UserSchemas:
        async with self.session.begin():
            return await self.create_user(data)

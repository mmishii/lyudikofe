from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.usecase.food.schemas import ResponseAllFood
from dataclasses import dataclass



@dataclass(slots=True, frozen=True, kw_only=True)
class GetFoodByIdUsecase(Usecase[UUID, ResponseAllFood]):
    session: AsyncSession

    async def __call__(self, data_id: UUID) -> ResponseAllFood:
        async with self.session.begin():
            # создание записи в самой корзине

            # создание записи в корзин продукта

            # создание записи в кастомах продуктах

            # возвращение итогов

            return



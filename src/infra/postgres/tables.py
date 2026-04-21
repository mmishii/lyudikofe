import uuid
from datetime import datetime
from sqlalchemy import UUID
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Annotated

uuid_pk = Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )]

created_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]
updated_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]

class BaseDBModel(DeclarativeBase):
    __tablename__: str
    __table_args__: dict[str, str] | tuple = {'schema': 'db_schema'}

    @classmethod
    def group_by_fields(cls, exclude: list[str] | None = None) -> list:
        payload = []
        if not exclude:
            exclude = []

        for column in cls.__table__.columns:
            if column.key in exclude:
                continue

            payload.append(column)

        return payload


# Пользователь 
class UsersModel(BaseDBModel):
    __tablename__ = 'users'
    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

# Статус
class StatusesModel(BaseDBModel):
    __tablename__ = 'statuses'
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        primary_key=True,)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

# Заказ
class OrdersModel(BaseDBModel):
    __tablename__ = 'orders'
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.users.id"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(255),        
        ForeignKey("db_schema.statuses.name"),
        nullable=False,
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    payment_method: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

# Закз продуктов
class OrderProductsModel(BaseDBModel):
    __tablename__ = 'order_products'
    id: Mapped[uuid_pk]
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.orders.id"),
        nullable=False,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.drinks.id" or "db_schema.foods.id" or"db_schema.ingredients.id"),
        nullable=False,
    )
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# Кастомные
class CustomsModel(BaseDBModel):
    __tablename__ = 'customs'
    id: Mapped[uuid_pk]
    ingredient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.ingredients.id"),
        nullable=False,
    )
    order_product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.orders.id"),
        nullable=False,
        
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# Изображения
class ImagesModel(BaseDBModel):
    __tablename__ = 'images'
    id: Mapped[uuid_pk]
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.drinks.id" or "db_schema.foods.id" or"db_schema.ingredients.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

# Напитки
class DrinksModel(BaseDBModel):
    __tablename__ = 'drinks'
    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True)
    season: Mapped[str] = mapped_column(String(100),
        ForeignKey("db_schema.seasons.name"), nullable=True)
    category: Mapped[str] = mapped_column(String(100), 
        ForeignKey("db_schema.categories.name"), nullable=True)
    macros_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.macros.id"),
        nullable=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

#Price
class PricesModel(BaseDBModel):
    __tablename__ = 'prices'
    id: Mapped[uuid_pk]
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.drinks.id" or "db_schema.foods.id" or "db_schema.ingredients.id"),
        nullable=False,
    )
    price: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# Сезоны
class SeasonsModel(BaseDBModel):
    __tablename__ = 'seasons'
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        primary_key=True,)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# Категории
class CategoriesModel(BaseDBModel):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        primary_key=True,)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

# кбжу
class MacrosModel(BaseDBModel):
    __tablename__ = 'macros'
    id: Mapped[uuid_pk]
    unit_kkal: Mapped[float] = mapped_column(nullable=False)
    unit_proteins: Mapped[float] = mapped_column(nullable=False)
    unit_carbs: Mapped[float] = mapped_column(nullable=False)
    unit_fats: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

# Еда
class FoodModel(BaseDBModel):
    __tablename__ = 'food'
    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True)
    category: Mapped[str] = mapped_column(String(100),
        ForeignKey("db_schema.categories.name"), nullable=True)
    macros_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.macros.id"),
        nullable=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# Ингредиенты
class IngredientsModel(BaseDBModel):
    __tablename__ = 'ingredients'
    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True)
    category: Mapped[str] = mapped_column(String(100),
        ForeignKey("db_schema.categories.name"), nullable=True)
    macros_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.macros.id"),
        nullable=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# Избранные кастомные напитки
class FavoriteCostumesModel(BaseDBModel):
   
    __tablename__ = 'favorite_customs'
    id: Mapped[uuid_pk]
    ingredient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.ingredients.id"),
        nullable=False,
    )
    favorite_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.favorite.id"),
        nullable=False,
        
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# Избранное
class FavoriteModel(BaseDBModel):
    __tablename__ = 'favorite'
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.users.id"),
        nullable=False,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.drinks.id" or "db_schema.foods.id" or"db_schema.ingredients.id"),
        nullable=False,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# Корзина
class CartModel(BaseDBModel):
    __tablename__ = 'cart'
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("db_schema.users.id"),
        nullable=False,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
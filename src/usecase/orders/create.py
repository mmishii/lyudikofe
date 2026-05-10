from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.auth import AuthSchema
from src.usecase.base import Usecase
from dataclasses import dataclass
from src.usecase.orders.schemas import RequestOrderSchema
from src.infra.postgres.tables import CustomsOrderModel, OrdersModel, OrderProductsModel
from src.infra.postgres.gateways.base import CreateReturningGate, DeleteGate
from src.application.schemas.custom_order import CreateCustomOrderProductSchema, CustomOrderProductSchema
from src.application.schemas.orders import OrderProductSchema, OrderSchema
from src.application.schemas.order_products import CreateOrderProductSchema, OrderProductSchema
from src.infra.postgres.tables import CartModel, CustomsCartModel
from src.usecase.orders.schemas import ResponseOrderSchema, ResponseProductSchema



@dataclass(slots=True, frozen=True, kw_only=True)
class CreateOrderUsecase(Usecase[RequestOrderSchema, ResponseOrderSchema]):
    session: AsyncSession
    user: AuthSchema
    create_order: CreateReturningGate[OrdersModel, OrderSchema, OrderSchema]
    create_order_product: CreateReturningGate[OrderProductsModel, CreateOrderProductSchema, OrderProductSchema]
    create_custom_order_product: CreateReturningGate[CustomsOrderModel, CreateCustomOrderProductSchema, CustomOrderProductSchema]
    delete_cart: DeleteGate[CartModel]
    delete_custom_cart: DeleteGate[CustomsCartModel]


    async def __call__(self, data: RequestOrderSchema) -> ResponseOrderSchema:
        async with self.session.begin():
            order = await self.create_order(
                OrderSchema(
                    user_id=self.user.id,
                    status=data.status,
                    count=data.count,
                    price=data.price,
                    comment=data.comment,
                    payment_method=data.payment_method
                )
            )
            products = []
            for product in data.products:
                order_product = await self.create_order_product(
                    CreateOrderProductSchema(
                        id=order_product.id,
                        order_id=order.id,
                        product_id=product.product_id,
                        quantity=product.quantity,
                        unit_price=product.unit_price
                    )
                )

                customs = []
                for custom in product.custom_products:
                    cutom_ = await self.create_custom_order_product(
                        CreateCustomOrderProductSchema(
                            id=custom.id,
                            order_id=order.id,
                            ingredient_id=custom.ingredient_id,
                            order_product_id=order_product.id
                        )
                    )
                    await self.delete_custom_cart(custom.id)
                    customs.append(cutom_)
                products.append(
                    ResponseProductSchema(
                        id=order_product.id,
                        order_id=order.id,
                        product_id=product.product_id,
                        quantity=product.quantity,
                        unit_price=product.unit_price,
                        custom_products=customs
                    )
                )

                await self.delete_cart(product.id)
            return ResponseOrderSchema(
                id=order.id,
                user_id=order.user_id,
                status=order.status,
                count=order.count,
                price=order.price,
                comment=order.comment,
                payment_method=order.payment_method,
                created_at=order.created_at,
                updated_at=order.updated_at,
                products=products
            )

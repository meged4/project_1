from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.orders.models import Orders
from sqlalchemy import insert, select, delete


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def add_order(cls, user_id,
                        tools_id,
                        quantity,
                        final_price,):
        async with async_session_maker() as session:
            add_order_for_user = insert(Orders).values(user_id=user_id,
                                                       tools_id=tools_id,
                                                       quantity=quantity,
                                                       final_price=final_price,
                                                       ).returning(Orders)
            result = await session.execute(add_order_for_user)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete_order(cls, id):
        async with async_session_maker() as session:
            query = delete(Orders).filter_by(id=id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_user_orders(cls, user_id):
        async with async_session_maker() as session:
            query = select(Orders).filter_by(user_id=user_id)
            result = await session.execute(query)
            return result.scalars().all()


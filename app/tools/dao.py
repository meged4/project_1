from app.dao.base import BaseDAO
from app.exceptions import EmptyOrderException, ToolNotAvailableException
from app.tools.models import Tools
from app.database import async_session_maker
from sqlalchemy import select, and_, insert, update


class ToolsDAO(BaseDAO):
    model = Tools

    @classmethod
    async def find_tools_by_price_and_tool_name(cls, name, price_down, price_up):
        async with async_session_maker() as session:
            query = select(Tools).where(
                                        and_(Tools.model_name == name,
                                             Tools.price_2_3 > price_down,
                                             Tools.price_2_3 < price_up)
                                        )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_new_tool(cls, **kwargs):
        async with async_session_maker() as session:
            query = insert(Tools).values(**kwargs).returning(Tools)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def find_tool_by_id(cls, tool_id):
        async with async_session_maker() as session:
            query = select(Tools).filter_by(id=tool_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def return_quantity_for_tool(cls, tool_id, quantity):
        async with async_session_maker() as session:
            query = update(Tools).filter_by(id=tool_id).values(quantity=Tools.quantity+quantity)
            res = await session.execute(query)
            await session.commit()
            return res

    @classmethod
    async def tool_quantity_for_order(cls, tool_id, order_quantity):
        async with async_session_maker() as session:
            query1 = select(Tools.quantity).filter_by(id=tool_id)
            max_quantity_for_order = await session.execute(query1)
            max_quantity_for_order = max_quantity_for_order.scalar_one_or_none()
            if max_quantity_for_order == 0:
                raise ToolNotAvailableException
            elif order_quantity > max_quantity_for_order:
                print(f"Quantity changed from {order_quantity} to {max_quantity_for_order}")
                order_quantity = max_quantity_for_order

            query2 = update(Tools).filter_by(id=tool_id).values(quantity=Tools.quantity-order_quantity).returning(Tools)
            await session.execute(query2)
            await session.commit()
            return order_quantity


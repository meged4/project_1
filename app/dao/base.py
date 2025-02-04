from app.database import async_session_maker
from sqlalchemy import select, insert


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

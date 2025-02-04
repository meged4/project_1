from app.dao.base import BaseDAO
from sqlalchemy import select, insert, update
from app.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def find_by_email(cls, email):
        async with async_session_maker() as session:
            query = select(Users).filter_by(email=email)
            result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def add_new_client(cls, **kwargs):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def change_password(cls, user_id, new_hashed_password):
        async with async_session_maker() as session:
            query = update(Users).filter_by(id=user_id).values(hashed_password=new_hashed_password)
            res = await session.execute(query)
            await session.commit()

    @classmethod
    async def change_email(cls, user_id, new_email):
        async with async_session_maker() as session:
            query = update(Users).filter_by(id=user_id).values(email=new_email)
            res = await session.execute(query)
            await session.commit()


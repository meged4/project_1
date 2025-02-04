from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.moderators.models import Moderators
from sqlalchemy import insert, select


class ModeratorsDAO(BaseDAO):
    model = Moderators

    @classmethod
    async def add_moderator(cls, email, hashed_password):
        async with async_session_maker() as session:
            query = insert(Moderators).values(email=email, hashed_password=hashed_password)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def show_moderators(cls):
        async with async_session_maker() as session:
            query = select(Moderators.email)
            result = await session.execute(query)
            return result.scalars().all()
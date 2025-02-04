from app.database import Base
from sqlalchemy import Column, String, Integer


class Moderators(Base):
    __tablename__ = "moderators"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

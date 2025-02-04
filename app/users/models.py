from app.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String)

    order = relationship("Orders", back_populates="user")

    def __str__(self):
        return f"User: {self.name}, email: {self.email}"

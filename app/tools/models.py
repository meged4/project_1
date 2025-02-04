from app.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Tools(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    fabricator = Column(String)
    model_name = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    price_2_3 = Column(Integer)
    price_4_6 = Column(Integer)
    price_7_10 = Column(Integer)
    price_11_20 = Column(Integer)
    price_21_50 = Column(Integer)
    price_more_then_50 = Column(Integer)

    order = relationship("Orders", back_populates="tool")

    def __str__(self):
        return f"{self.model_name} {self.fabricator}"

from datetime import datetime, date, time
from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Time, Date, Computed
from sqlalchemy.orm import relationship


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    tools_id = Column(Integer, ForeignKey("tools.id"))
    quantity = Column(Integer, nullable=False)
    date = Column(Date, default=datetime.now())
    time = Column(Time, default=datetime.now())
    final_price = Column(Integer, nullable=True)
    total_amount = Column(Integer, Computed("quantity*final_price"), nullable=True)

    user = relationship("Users", back_populates="order")
    tool = relationship("Tools", back_populates="order")

    def __str__(self):
        return f"Заказ № {self.id} на дату: {self.date}"

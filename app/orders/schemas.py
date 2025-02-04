from pydantic import BaseModel
from datetime import date, time


class SOrder(BaseModel):
    id: int
    user_id: int
    tools_id: int
    quantity: int
    date: date
    time: time
    final_price: int
    total_amount: int

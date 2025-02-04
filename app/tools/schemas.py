from pydantic import BaseModel


class SToolsAdd(BaseModel):
    fabricator: str
    model_name: str
    description: str
    quantity: int
    price_2_3: int
    price_4_6: int
    price_7_10: int
    price_11_20: int
    price_21_50: int
    price_more_then_50: int

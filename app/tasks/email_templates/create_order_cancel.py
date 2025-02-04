from pydantic import EmailStr
from app.config import settings
from email.message import EmailMessage


def create_order_cancel_message(email_to: EmailStr, cancel, order, tool_name):
    email = EmailMessage()
    email["subject"] = f"Вы оформили отмену заказа"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to
    email.set_content(
        f"""<div><b>Вы оформили отмену заказа: {tool_name} в количестве {order.quantity} штук по цене {order.final_price} рублей за штуку</b></div>
    <hr>
                           <b>Суммарная цена за весь заказ {order.total_amount} рублей</b>
                            <hr>
                            <b>Время оформления возврата {cancel['date']} {cancel['time']}""", subtype="html")
    return email

from pydantic import EmailStr
from email.message import EmailMessage
from app.database import settings


def create_confirmation_template_dict(email_to: EmailStr, order: dict, tool_name):
    email = EmailMessage()
    email["subject"] = f"Вы оформили заказ {order['date']} {order['time']}"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to
    email.set_content(f"""<b>Вы оформили заказ: {tool_name} в количестве {order['quantity']} штук по цене {order['final_price']} за штуку</b>
                           <b>Суммарная цена за весь заказ {order['total_amount']}</b> """, subtype="html")
    return email


def create_order_confirmation_template(email_to: EmailStr, order, tool_name):
    email = EmailMessage()
    email["subject"] = f"Вы оформили заказ {order.date} {order.time}"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to
    email.set_content(f"""<div><b>Вы оформили заказ: {tool_name} в количестве {order.quantity} штук по цене {order.final_price} рублей за штуку</b></div>
    <hr>
                           <b>Суммарная цена за весь заказ {order.total_amount} рублей</b> """, subtype="html")
    return email


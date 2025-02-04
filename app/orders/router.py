from fastapi import APIRouter, Depends, BackgroundTasks
from app.auth.dependencies import get_current_user
from app.exceptions import EmptyOrderException, DontExistOrderException
from app.orders.calculate_summa import calculate_order_amount
from app.orders.dao import OrdersDAO
from app.tasks.email_templates.confirm_order import create_order_confirmation_template
from app.tasks.email_templates.create_order_cancel import create_order_cancel_message
from app.tasks.email_templates.email_templates import EmailTemplate
from app.tools.dao import ToolsDAO
from datetime import date, time, datetime

router = APIRouter(prefix='/orders',
                   tags=['Заказы клиентов'])


@router.get("/get_orders")
async def get_user_orders(user=Depends(get_current_user)):
    orders = await OrdersDAO.find_user_orders(user.id)
    if not orders:
        return "Пусто"
    return orders


@router.get("/add_order")
async def add_user_order(tools_id: int,
                         quantity: int,
                         background_tasks: BackgroundTasks,
                         user=Depends(get_current_user),):
    if quantity == 0:
        raise EmptyOrderException
    checked_quantity = await ToolsDAO.tool_quantity_for_order(tools_id, quantity)
    final_price = await calculate_order_amount(checked_quantity, tools_id)
    order = await OrdersDAO.add_order(user.id, tools_id, checked_quantity, final_price)
    tool = await ToolsDAO.find_one(id=tools_id)
    #order_dict = parse_obj_as(SOrder, order)
    #background_tasks.add_task(EmailTemplate.sent_message_confirmation(create_order_confirmation_template, user.email, order, tool.model_name))
    return order


@router.get("/cancel_order")
async def cancel_user_order(order_id: int, background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    order = await OrdersDAO.find_one(id=order_id, user_id=user.id)
    if not order:
        raise DontExistOrderException
    return_quantity = order.quantity
    tool_id = order.tools_id
    tool_from_order = await ToolsDAO.return_quantity_for_tool(tool_id, return_quantity)
    cancel = {"date": date.today(), "time": datetime.now().strftime("%H:%M:%S")}
    await OrdersDAO.delete_order(order_id)
    #background_tasks.add_task(EmailTemplate.sent_message_confirmation(create_order_cancel_message, user.email, cancel, order, tool_from_order))
    return "Order cancelled"


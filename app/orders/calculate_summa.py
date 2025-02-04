from app.tools.dao import ToolsDAO


async def calculate_order_amount(quantity, tool_id):
    tool = await ToolsDAO.find_tool_by_id(tool_id)
    if quantity <= 3:
        price = tool.price_2_3
    elif quantity <= 6:
        price = tool.price_2_3
    elif quantity <= 10:
        price = tool.price_7_10
    elif quantity <= 20:
        price = tool.price_11_20
    elif quantity <= 50:
        price = tool.price_21_50
    else:
        price = tool.price_more_then_50
    return price


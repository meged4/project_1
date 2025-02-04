from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_moderator
from app.exceptions import NotFoundToolsException
from app.tools.dao import ToolsDAO
from app.tools.schemas import SToolsAdd

router = APIRouter(prefix="/tools",
                   tags=["Инструменты"])


@router.get("/get_tools_list")
async def get_tools(tool_name: str,
                    price_lowest: int,
                    price_uppest: int, ):
    find_tools = await ToolsDAO.find_tools_by_price_and_tool_name(tool_name, price_lowest, price_uppest)
    if not find_tools:
        raise NotFoundToolsException
    return find_tools


@router.post("/add_tool")
async def add_tool(params: SToolsAdd, admin=Depends(get_current_moderator)):
    tool = await ToolsDAO.add_new_tool(**params.dict())
    if not tool:
        return "Fail"
    else:
        return tool

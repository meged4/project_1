import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqladmin import Admin
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from app.admin.auth import authentication_backend
from app.database import engine
from app.admin.views import ToolsAdmin, UsersAdmin, ModersAdmin, OrdersAdmin
from app.users.router import router as users_router
from app.tools.router import router as tools_router
from app.orders.router import router as orders_router
from app.moderators.router import router as moderator_router

app = FastAPI()
app.include_router(users_router)
app.include_router(tools_router)
app.include_router(orders_router)
app.include_router(moderator_router)

admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)  #
admin.add_view(ToolsAdmin)
admin.add_view(UsersAdmin)
admin.add_view(ModersAdmin)
admin.add_view(OrdersAdmin)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def get_main_page(request: Request):
    return templates.TemplateResponse(name="main_page.html", context={'request': request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

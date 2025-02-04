from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth.auth import create_access_token_for_moderators, authenticate_moder
from app.auth.dependencies import get_current_moderator
from app.moderators.dao import ModeratorsDAO


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        moderator = await authenticate_moder(email=username, password=password)
        if moderator:
            token = await create_access_token_for_moderators({'sub': username})
            request.session.update({"moder_access_token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        token = request.session.get("moder_access_token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        moderator = await get_current_moderator(token)
        if not moderator:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True


authentication_backend = AdminAuth(secret_key="...")

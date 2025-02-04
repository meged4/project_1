from fastapi import APIRouter, Depends, Response, Request

from app.auth.auth import get_password_hash, authenticate_moder, create_access_token_for_moderators
from app.auth.dependencies import get_current_user, get_current_moderator
from app.exceptions import ModerSecretKeyException, ModerAlreadyRegister, NotFindUsersException
from app.moderators.dao import ModeratorsDAO
from app.users.dao import UsersDAO
from app.moderators.schemas import SModeratorsLogin, SModeratorsRegister
from app.config import settings


router = APIRouter(prefix="/moder",
                   tags=["Moderators"])


@router.post("/get_info")
async def get_info(user=Depends(get_current_user)):
    admins = await ModeratorsDAO.show_moderators()
    return admins


@router.post("/register_admin")
async def register_admin(moder_info: SModeratorsRegister):
    if settings.SECRET_WORD != moder_info.secret_word:
        raise ModerSecretKeyException
    moderator = await ModeratorsDAO.find_one(email=moder_info.email)
    if moderator:
        raise ModerAlreadyRegister
    hashed_password = await get_password_hash(moder_info.password)
    await ModeratorsDAO.add_moderator(email=moder_info.email, hashed_password=hashed_password)
    return "Success!"


@router.post("/login_admin")
async def login_moder(moder_info: SModeratorsLogin, response: Response):
    moderator = await authenticate_moder(email=moder_info.email, password=moder_info.password)
    access_token = await create_access_token_for_moderators({"sub": moderator.email})
    response.set_cookie("moder_access_token", access_token, httponly=True)
    return "Successfully login, moderator!"


@router.post("/logout_admin")
async def logout_moder(response: Response, moder=Depends(get_current_moderator)):
    response.delete_cookie("moder_access_token", httponly=True)
    return "You successfully logout, moderator"


@router.get("/show_users")
async def show_clients(admin=Depends(get_current_moderator)):
    clients = await UsersDAO.find_all()
    if not clients:
        raise NotFindUsersException
    return clients

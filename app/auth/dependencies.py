from fastapi import Request, Depends
from jose import JWTError
from datetime import datetime, timedelta

from app.exceptions import IncorrectTokenFormat, NotFoundTokenFormat, UserIsNotPresentException, TokenExpiredException, \
    ModerIsNotPresentException
from app.moderators.dao import ModeratorsDAO
from app.users.dao import UsersDAO
from app.auth.auth import decode_access_token_and_get_user_id, decode_access_token_and_get_moder_info


async def get_token(request: Request):
    token = request.cookies.get('client_access_token')
    if not token:
        raise NotFoundTokenFormat
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = await decode_access_token_and_get_user_id(token)
    except JWTError:
        raise IncorrectTokenFormat
    expire: str = payload.get('exp')
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException
    user_id: int = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_one(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user


async def get_moders_token(request: Request):
    token = request.cookies.get('moder_access_token')
    if not token:
        raise NotFoundTokenFormat
    return token


async def get_current_moderator(token: str = Depends(get_moders_token)):
    try:
        payload = await decode_access_token_and_get_moder_info(token)
    except JWTError:
        raise IncorrectTokenFormat
    expire: str = payload.get('exp')
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException
    email: str = payload.get('sub')
    if not email:
        raise ModerIsNotPresentException
    moder = await ModeratorsDAO.find_one(email=email)
    if not moder:
        raise ModerIsNotPresentException
    return moder

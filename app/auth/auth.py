from passlib.context import CryptContext
from datetime import date, datetime, timedelta
from jose import jwt
from app.config import settings
from pydantic import EmailStr

from app.exceptions import NotFoundModerException, IncorrectPasswordException
from app.moderators.dao import ModeratorsDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_password_hash(password) -> str:
    return pwd_context.hash(password)


async def verify_password(entered_password, hashed_password) -> bool:
    return pwd_context.verify(entered_password, hashed_password)


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def decode_access_token_and_get_user_id(token):
    decoded_token = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    return decoded_token


async def create_access_token_for_moderators(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(hours=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def decode_access_token_and_get_moder_info(token: str):
    decoded_token = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    return decoded_token


async def authenticate_moder(email: EmailStr, password: str):
    moderator = await ModeratorsDAO.find_one(email=email)
    if not moderator:
        raise NotFoundModerException
    flag = await verify_password(password, moderator.hashed_password)
    if not flag:
        raise IncorrectPasswordException
    return moderator

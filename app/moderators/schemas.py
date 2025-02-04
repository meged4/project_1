from pydantic import BaseModel, EmailStr


class SModeratorsRegister(BaseModel):
    email: EmailStr
    password: str
    secret_word: str


class SModeratorsLogin(BaseModel):
    email: EmailStr
    password: str

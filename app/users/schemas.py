from pydantic import BaseModel, EmailStr


class SUsersRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone_number: str


class SUsersLogin(BaseModel):
    email: EmailStr
    password: str


class SUserChangePassword(BaseModel):
    current_password: str
    new_password: str


class SUserChangeEmail(BaseModel):
    new_email: EmailStr
    password: str

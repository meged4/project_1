from fastapi import APIRouter, Depends, Response, BackgroundTasks
from app.auth.dependencies import get_current_user
from app.exceptions import UserAlreadyRegister, NotFindUserException, IncorrectPasswordException, NotFindUsersException, \
    PasswordNotChangedException, EmailBelongAnotherException, EmailNotChangedException
from app.orders.dao import OrdersDAO
from app.tools.dao import ToolsDAO
from app.users.schemas import SUsersRegister, SUsersLogin, SUserChangePassword, SUserChangeEmail
from app.users.dao import UsersDAO
from app.auth.auth import get_password_hash, verify_password, create_access_token


router = APIRouter(prefix='/client',
                   tags=["Auth & Register & Settings Clients"])


@router.post('/register')
async def register_user(user_data: SUsersRegister):
    user = await UsersDAO.find_by_email(email=user_data.email)
    if user:
        raise UserAlreadyRegister
    hashed_password = await get_password_hash(user_data.password)
    await UsersDAO.add_new_client(
                                    email=user_data.email,
                                    hashed_password=hashed_password,
                                    name=user_data.name,
                                    phone_number=user_data.phone_number,
                                    )

    return "You successfully register!"


@router.post("/login")
async def login_user(user_data: SUsersLogin, response: Response):
    user = await UsersDAO.find_by_email(user_data.email)
    if not user:
        raise NotFindUserException
    if not await verify_password(user_data.password, user.hashed_password):
        raise IncorrectPasswordException
    access_token = await create_access_token({'sub': str(user.id)})
    response.set_cookie("client_access_token", access_token, httponly=True)
    return "You successfully login!"


@router.post("/logout")
async def logout_user(response: Response, user_data=Depends(get_current_user)):
    response.delete_cookie("client_access_token", httponly=True)
    return "Successfully logout!"


@router.get("/about")
async def get_client_info(user=Depends(get_current_user)):
    client_info = await UsersDAO.find_one(id=user.id)
    return client_info


@router.post("/change_password")
async def change_password(user_data: SUserChangePassword, background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    check_password = await verify_password(user_data.current_password, user.hashed_password)
    if not check_password:
        raise IncorrectPasswordException
    old_new_no_diff = await verify_password(user_data.new_password, user.hashed_password)
    if old_new_no_diff:
        raise PasswordNotChangedException
    hashed_password = await get_password_hash(user_data.new_password)
    await UsersDAO.change_password(user.id, hashed_password)
    #background_tasks.add_task()
    return "Successfully changed password"


@router.post("/change_email")
async def change_email(user_data: SUserChangeEmail, background_tasks: BackgroundTasks, user_info=Depends(get_current_user)):
    user = await UsersDAO.find_by_email(user_info.email)
    user_check_email = await UsersDAO.find_by_email(user_data.new_email)
    if user_data.new_email == user_info.email:
        raise EmailNotChangedException
    if user_check_email:
        raise EmailBelongAnotherException
    if not user:
        raise NotFindUsersException
    if not await verify_password(user_data.password, user.hashed_password):
        raise IncorrectPasswordException
    await UsersDAO.change_email(user.id, user_data.new_email)
    #background_tasks.add_task()
    return "Successfully changed email"

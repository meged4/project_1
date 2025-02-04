from fastapi import HTTPException, status


class Ex(HTTPException):
    detail = ""
    status_code = 500

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyRegister(Ex):
    detail = "Пользователь уже зарегистрирован"
    status_code = status.HTTP_409_CONFLICT


class NotFindUserException(Ex):
    detail = "Неверно введена почта или данный пользователь не зарегистрирован"
    status_code = status.HTTP_404_NOT_FOUND


class IncorrectPasswordException(Ex):
    detail = "Неверный пароль"
    status_code = status.HTTP_409_CONFLICT


class IncorrectTokenFormat(Ex):
    detail = "Неверный формат токена"
    status_code = status.HTTP_409_CONFLICT


class NotFoundTokenFormat(Ex):
    detail = "Токен отсутствует"
    status_code = status.HTTP_409_CONFLICT


class NotFoundModerException(Ex):
    detail = "С данной почтой модераторов не зарегистрировано"
    status_code = status.HTTP_409_CONFLICT


class ModerAlreadyRegister(Ex):
    detail = "Модератор уже зарегистрирован"
    status_code = status.HTTP_409_CONFLICT


class TokenExpiredException(Ex):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class TokenAbsentException(Ex):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class UserIsNotPresentException(Ex):
    status_code = status.HTTP_401_UNAUTHORIZED


class ModerIsNotPresentException(Ex):
    status_code = status.HTTP_401_UNAUTHORIZED


class NotFoundToolsException(Ex):
    detail = "Инструментов по таким параметрам не найдено"
    status_code = status.HTTP_404_NOT_FOUND


class ModerSecretKeyException(Ex):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Секретный ключ неверен"


class NotFindUsersException(Ex):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователей не найдено"


class EmptyOrderException(Ex):
    status_code = status.HTTP_409_CONFLICT
    detail = "В заказе должна быть минимум одна единица товара"


class ToolNotAvailableException(Ex):
    status_code = status.HTTP_409_CONFLICT
    detail = "Товар закончился"


class DontExistOrderException(Ex):
    status_code = status.HTTP_409_CONFLICT
    detail = "Такого заказа нет"


class PasswordNotChangedException(Ex):
    status_code = status.HTTP_409_CONFLICT
    detail = "Новый пароль не должен совпадать со старым паролем"


class EmailBelongAnotherException(Ex):
    detail = "Почта принадлежит другому пользователю"
    status_code = status.HTTP_409_CONFLICT


class EmailNotChangedException(Ex):
    status_code = status.HTTP_409_CONFLICT
    detail = "Новая почта не должна совпадать со старой почтой"

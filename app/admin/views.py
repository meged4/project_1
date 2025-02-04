from sqladmin import ModelView

from app.orders.models import Orders
from app.tools.models import Tools
from app.users.models import Users
from app.moderators.models import Moderators


class ToolsAdmin(ModelView, model=Tools):
    name = "Инструмент"
    name_plural = "Инструменты"
    column_list = [c.name for c in Tools.__table__.c] + [Tools.order]
    column_searchable_list = [Tools.fabricator, Tools.model_name]


class UsersAdmin(ModelView, model=Users):
    column_exclude_list = [Users.hashed_password]
    column_details_exclude_list = [Users.hashed_password]
    name = "Пользователь"
    name_plural = "Пользователи"


class ModersAdmin(ModelView, model=Moderators):
    column_exclude_list = [Moderators.hashed_password]
    name = "Администратор"
    name_plural = "Администраторы"


class OrdersAdmin(ModelView, model=Orders):
    name = "Заказ"
    name_plural = "Заказы"
    #column_list = [Orders.tool, Orders.user]+[c.name for c in Orders.__table__.c]
    column_exclude_list = [Orders.id, Orders.user_id, Orders.tools_id]

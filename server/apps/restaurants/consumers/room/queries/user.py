from channels.db import database_sync_to_async

from apps.users.functions import check_role_employee
from apps.users.models import Employee, User


class UserQueries:

    @staticmethod
    @database_sync_to_async
    def is_client(user: User) -> bool:
        return user.is_client

    @staticmethod
    @database_sync_to_async
    def check_role_employee_connect(user) -> bool:
        return any([
            check_role_employee(user, Employee.Roles.WAITER),
            check_role_employee(user, Employee.Roles.CHEF),
            check_role_employee(user, Employee.Roles.SOUS_CHEF),
            check_role_employee(user, Employee.Roles.COOK),
            check_role_employee(user, Employee.Roles.MANAGER),
        ])

    @staticmethod
    @database_sync_to_async
    def check_role_employee_cant_create_order(user) -> bool:
        return any([
            check_role_employee(user, Employee.Roles.CHEF),
            check_role_employee(user, Employee.Roles.SOUS_CHEF),
            check_role_employee(user, Employee.Roles.COOK),
        ])

    @staticmethod
    @database_sync_to_async
    def check_role_employee_cant_edit_order(user) -> bool:
        return any([
            check_role_employee(user, Employee.Roles.CHEF),
            check_role_employee(user, Employee.Roles.SOUS_CHEF),
            check_role_employee(user, Employee.Roles.COOK),
        ])

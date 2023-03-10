from rest_framework import permissions

from apps.users.models import Employee
from apps.users.functions import check_role_employee


class OrderAndDishPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return not request.user.is_client

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PATCH", "PUT"):
            return any([
                check_role_employee(request.user, Employee.Roles.COOK),
                check_role_employee(request.user, Employee.Roles.CHEF),
                check_role_employee(request.user, Employee.Roles.SOUS_CHEF),
                check_role_employee(request.user, Employee.Roles.WAITER),
            ])
        if request.method == "DELETE":
            return check_role_employee(request.user, Employee.Roles.WAITER)

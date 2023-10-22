from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class OrderAndDishPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return not request.user.is_client

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.employee.restaurant != obj.order.employee.restaurant:
            return False
        if request.method in ("PATCH", "PUT"):
            return any([
                check_role_employee(request.user, Employee.Roles.COOK),
                check_role_employee(request.user, Employee.Roles.CHEF),
                check_role_employee(request.user, Employee.Roles.SOUS_CHEF),
                check_role_employee(request.user, Employee.Roles.WAITER),
            ])

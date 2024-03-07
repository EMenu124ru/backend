from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class IngredientPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method == "GET":
            return (
                request.user.is_authenticated and
                check_role_employee(request.user, Employee.Roles.CHEF)
            )
        return False


class DishPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.method == "GET"

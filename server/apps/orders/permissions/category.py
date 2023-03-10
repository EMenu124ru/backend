from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class CategoryPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method == "GET":
            return True
        if request.user.is_authenticated:
            return check_role_employee(request.user, Employee.Roles.MANAGER)
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        if (
            request.method in ("PUT", "PATCH", "DELETE")
            and request.user.is_authenticated
        ):
            return check_role_employee(request.user, Employee.Roles.MANAGER)
        return True

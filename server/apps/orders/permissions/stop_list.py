from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class StopListPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated or request.user.is_client:
            return False
        if request.method == "GET" and any([
            check_role_employee(request.user, Employee.Roles.MANAGER),
            check_role_employee(request.user, Employee.Roles.WAITER),
        ]):
            return True
        if request.method == "POST":
            return check_role_employee(request.user, Employee.Roles.MANAGER)
        return check_role_employee(request.user, Employee.Roles.MANAGER)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "DELETE":
            return check_role_employee(request.user, Employee.Roles.MANAGER)

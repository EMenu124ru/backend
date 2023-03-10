from rest_framework import permissions

from apps.users.models import Employee
from apps.users.functions import check_role_employee


class StopListPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.user.is_client:
            return False
        if request.method == "GET" and any([
            check_role_employee(request.user, Employee.Roles.COOK),
            check_role_employee(request.user, Employee.Roles.WAITER),
        ]):
            return True
        if request.method == "POST":
            return check_role_employee(request.user, Employee.Roles.COOK)
        return check_role_employee(request.user, Employee.Roles.COOK)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "DELETE":
            return check_role_employee(request.user, Employee.Roles.COOK)

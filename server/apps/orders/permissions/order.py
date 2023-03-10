from rest_framework import permissions

from apps.users.models import Employee
from apps.users.functions import check_role_employee


class OrderPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if all([
            request.method == "GET",
            view.action == "list",
            request.user.is_client,
        ]):
            return False
        if request.method == "POST":
            return check_role_employee(request.user, Employee.Roles.WAITER)
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "GET":
            if request.user.is_client:
                return obj.client.user == request.user
            return check_role_employee(request.user, Employee.Roles.WAITER)
        if request.method == "DELETE" and (
            check_role_employee(request.user, Employee.Roles.WAITER)
        ):
            return True
        if request.method in ("PUT", "PATCH"):
            return not request.user.is_client
        return False

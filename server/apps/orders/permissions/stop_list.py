from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class StopListPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        is_waiter = check_role_employee(request.user, Employee.Roles.WAITER)
        if request.method == "GET" and is_waiter:
            return True
        return check_role_employee(request.user, Employee.Roles.CHEF)

from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class ReservationPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        has_permissions = [
            check_role_employee(request.user, Employee.Roles.HOSTESS),
            check_role_employee(request.user, Employee.Roles.WAITER),
        ]
        if view.action == "list":
            return any(has_permissions)
        has_permissions.append(request.user.is_client)
        return any(has_permissions)

    def has_object_permission(self, request, view, obj) -> bool:
        is_client = request.user.is_client and obj.client and obj.client.id == request.user.client.id
        is_hostess = (
            check_role_employee(request.user, Employee.Roles.HOSTESS) and
            obj.restaurant == request.user.employee.restaurant
        )
        is_waiter = (
            check_role_employee(request.user, Employee.Roles.WAITER) and
            obj.restaurant == request.user.employee.restaurant
        )
        if request.method == "GET":
            return any([is_client, is_hostess, is_waiter])
        return is_hostess

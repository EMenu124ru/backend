from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class RestaurantAndOrderPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if all([
            request.method == "GET",
            view.action == "list",
            request.user.is_client,
        ]):
            return False
        if request.user.is_client:
            return True
        return any([
            check_role_employee(request.user, Employee.Roles.HOSTESS),
            check_role_employee(request.user, Employee.Roles.WAITER),
        ])

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "GET":
            return (
                obj.order.client.user == request.user
                or not request.user.is_client
            )
        if request.method in ("PUT", "PATCH", "DELETE"):
            if request.user.is_client:
                return False
            return any([
                check_role_employee(request.user, Employee.Roles.HOSTESS),
                check_role_employee(request.user, Employee.Roles.WAITER),
            ])
        return True

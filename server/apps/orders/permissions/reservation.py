from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class ReservationPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if all([
            request.method == "GET",
            view.action == "list",
        ]):
            return any([
                check_role_employee(request.user, Employee.Roles.HOSTESS),
                check_role_employee(request.user, Employee.Roles.WAITER),
            ])
        if request.method == "POST":
            return request.user.is_client
        return any([
            request.user.is_client,
            check_role_employee(request.user, Employee.Roles.HOSTESS),
            check_role_employee(request.user, Employee.Roles.WAITER),
        ])

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PUT", "PATCH", "GET"):
            return any([
                request.user.is_client and obj.client and obj.client.user == request.user,
                (
                    check_role_employee(request.user, Employee.Roles.HOSTESS) and
                    obj.restaurant == request.user.employee.restaurant
                ),
                (
                    check_role_employee(request.user, Employee.Roles.WAITER) and
                    obj.restaurant == request.user.employee.restaurant
                ),
            ])
        return True

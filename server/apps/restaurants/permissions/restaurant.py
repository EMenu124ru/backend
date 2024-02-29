from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class RestaurantPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return any([
            check_role_employee(request.user, Employee.Roles.HOSTESS),
            check_role_employee(request.user, Employee.Roles.WAITER),
        ])

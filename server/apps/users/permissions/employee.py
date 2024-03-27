from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return check_role_employee(request.user, Employee.Roles.MANAGER)


class IsChef(permissions.BasePermission):

    def has_permission(self, request, view):
        return check_role_employee(request.user, Employee.Roles.CHEF)


class FromSameRestaurantEmployee(permissions.BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_client

    def has_object_permission(self, request, view, obj):
        return request.user.employee.restaurant.id == obj.restaurant.id


class FromSameRestaurantSchedule(IsManager):

    def has_object_permission(self, request, view, obj):
        return all([
            not request.user.is_client,
            check_role_employee(request.user, Employee.Roles.MANAGER),
            request.user.employee.restaurant.id == obj.employee.restaurant.id,
        ])

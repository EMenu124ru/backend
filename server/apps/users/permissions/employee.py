from rest_framework import permissions

from apps.users.functions import check_role_employee
from apps.users.models import Employee


class FromSameRestaurantEmployee(permissions.BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_client

    def has_object_permission(self, request, view, obj):
        return request.user.employee.restaurant.id == obj.restaurant.id


class FromSameRestaurantSchedule(permissions.BasePermission):

    def has_permission(self, request, view):
        return check_role_employee(request.user, Employee.Roles.MANAGER)

    def has_object_permission(self, request, view, obj):
        return request.user.employee.restaurant.id == obj.employee.restaurant.id

from rest_framework import permissions

from apps.users.models import Employee


class RestaurantPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_client:
            return False
        if request.user.employee.role == Employee.Roles.HOSTESS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.employee.restaurant.id == obj.id

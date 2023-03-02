from rest_framework import permissions

from apps.users.models import Employee
from apps.users.permissions import check_role_employee


class ReviewPermissions(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method == "GET":
            return True
        if request.user.is_authenticated:
            if any([
                check_role_employee(request.user, Employee.Roles.MANAGER),
                request.user.is_staff,
                request.user.is_client,
            ]):
                return True
        if all([
            request.method == "POST",
            request.user.is_client,
        ]):
            return True
        return False
    
    def has_object_permission(self, request, view, obj) -> bool:
        if all([
            request.method in ("PUT", "PATCH", "DELETE"),
            request.user.is_client,
            request.user == obj.client.user,
        ]):
            return True
        if request.method in ("DELETE") and any([
            check_role_employee(request.user, Employee.Roles.MANAGER),
            request.user.is_staff,
        ]):
            return True
        return False

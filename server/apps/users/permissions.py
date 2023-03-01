from rest_framework import permissions

from apps.users.models import User


def check_role_employee(user: User, role: str) -> bool:
    if user.is_client:
        return False
    if user.employee.role == role:
        return True
    return False


class IsCurrentUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj.user

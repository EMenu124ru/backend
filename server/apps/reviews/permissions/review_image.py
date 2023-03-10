from rest_framework import permissions

from apps.users.models import Employee
from apps.users.functions import check_role_employee


class ReviewImagePermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        return any([
            obj.review.client.user.id == request.user.id,
            check_role_employee(request.user, Employee.Roles.MANAGER),
            request.user.is_staff,
        ])

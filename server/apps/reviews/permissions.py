from rest_framework import permissions

from apps.users.models import Employee
from apps.users.permissions import check_role_employee

from apps.reviews.models import Review


class ReviewPermissions(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        has_permission_images = False
        if review := Review.objects.filter(id=view.kwargs.get("pk", None)):
            has_permission_images = review.first().client.user.id == request.user.id
        if request.method == "POST":
            if request.user.is_client:
                return any([
                    all([
                        view.action == "images",
                        has_permission_images,
                    ]),
                    view.action == "create",
                ])
            return False
        if any([
            check_role_employee(request.user, Employee.Roles.MANAGER),
            request.user.is_staff,
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
        if request.method == "DELETE" and any([
            check_role_employee(request.user, Employee.Roles.MANAGER),
            request.user.is_staff,
        ]):
            return True
        return False


class ReviewImagePermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.review.client.user.id == request.user.id

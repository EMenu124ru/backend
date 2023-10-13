from rest_framework import permissions


class IsCurrentUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            not request.user.is_authenticated and
            request.method == "POST" and
            view.action in ("create", "login")
        ):
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.is_authenticated:
            return request.user == obj.user
        return False

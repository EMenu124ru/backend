from rest_framework import permissions

from apps.users.models import Employee, User


class IsManager(permissions.BasePermission):

    def is_manager(self, user: User) -> bool:
        if user.is_client:
            return False
        if user.employee.role == Employee.Roles.MANAGER:
            return True
        return False

    def has_permission(self, request, view) -> bool:
        if request.method == "GET":
            return True
        return self.is_manager(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PUT", "PATCH", "DELETE"):
            return self.is_manager(request.user)
        return True


class IsWaiter(permissions.BasePermission):

    def is_waiter(self, user: User) -> bool:
        if user.is_client:
            return False
        if user.employee.role == Employee.Roles.WAITER:
            return True
        return False

    def has_permission(self, request, view) -> bool:
        if request.method == "GET":
            return True
        return self.is_waiter(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PUT", "PATCH", "DELETE"):
            return self.is_waiter(request.user)
        return True


class IsCook(permissions.BasePermission):

    def is_cook(self, user: User) -> bool:
        if user.is_client:
            return False
        if user.employee.role in (
            Employee.Roles.COOK,
            Employee.Roles.CHEF,
            Employee.Roles.BARTENDER,
        ):
            return True
        return False

    def has_permission(self, request, view) -> bool:
        if request.method == "GET":
            return True
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PUT", "PATCH"):
            return self.is_cook(request.user)
        if request.method == "GET":
            return True
        return False


class IsHostess(permissions.BasePermission):

    def is_hostess_or_client(self, user: User) -> bool:
        if user.is_client or user.employee.role == Employee.Roles.HOSTESS:
            return True
        return False

    def has_permission(self, request, view) -> bool:
        if request.method == "GET":
            return True
        return self.is_hostess_or_client(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PUT", "PATCH", "DELETE"):
            return self.is_hostess_or_client(request.user)
        return True

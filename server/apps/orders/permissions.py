from rest_framework import permissions

from apps.users.models import Employee, User


def check_role_employee(user: User, role: str) -> bool:
    if user.is_client:
        return False
    if user.employee.role == role:
        return True
    return False


class DishCategoryPermissions(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if all([
            view.basename == "dishes",
            view.action == "orders",
        ]):
            if not request.user.is_authenticated:
                return False
            return not request.user.is_client
        if request.method == "GET":
            return True
        if request.user.is_authenticated:
            return check_role_employee(request.user, Employee.Roles.MANAGER)
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        if (
            request.method in ("PUT", "PATCH", "DELETE")
            and request.user.is_authenticated
        ):
            return check_role_employee(request.user, Employee.Roles.MANAGER)
        return True


class OrderPermissions(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if all([
            request.method == "GET",
            view.action == "list",
            request.user.is_client,
        ]):
            return False
        if request.method == "POST":
            return not request.user.is_client
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "DELETE" and not request.user.is_client:
            if request.user.employee.role in (
                Employee.Roles.WAITER,
                Employee.Roles.HOSTESS,
            ):
                return True
        if request.method in ("PUT", "PATCH", "GET"):
            return obj.client.user == request.user or not request.user.is_client
        return False


class RestaurantAndOrdersPermissions(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if all([
            request.method == "GET",
            view.action == "list",
            request.user.is_client,
        ]):
            return False
        return (
            request.user.is_client
            or request.user.employee.role == Employee.Roles.HOSTESS
        )

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "GET":
            return (
                obj.order.client.user == request.user
                or not request.user.is_client
            )
        if (
            request.method in ("PUT", "PATCH", "DELETE")
            and not request.user.is_client
        ):
            return any([
                request.user.employee.role == Employee.Roles.HOSTESS,
                request.user.employee.role == Employee.Roles.WAITER,
            ])
        return True

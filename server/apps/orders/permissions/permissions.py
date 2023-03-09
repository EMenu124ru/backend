from rest_framework import permissions

from apps.users.models import Employee
from apps.users.permissions import check_role_employee


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
        if all([
            request.method == "GET",
            view.action == "list",
            request.user.is_client,
        ]):
            return False
        if request.method == "POST":
            return check_role_employee(request.user, Employee.Roles.WAITER)
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "GET":
            if request.user.is_client:
                return obj.client.user == request.user
            return check_role_employee(request.user, Employee.Roles.WAITER)
        if request.method == "DELETE" and (
            check_role_employee(request.user, Employee.Roles.WAITER)
        ):
            return True
        if request.method in ("PUT", "PATCH"):
            return not request.user.is_client
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
        if request.user.is_client:
            return True
        return any([
            request.user.employee.role == Employee.Roles.HOSTESS,
            request.user.employee.role == Employee.Roles.WAITER,
        ])

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "GET":
            return (
                obj.order.client.user == request.user
                or not request.user.is_client
            )
        if request.method in ("PUT", "PATCH", "DELETE"):
            if request.user.is_client:
                return False
            return any([
                request.user.employee.role == Employee.Roles.HOSTESS,
                request.user.employee.role == Employee.Roles.WAITER,
            ])
        return True


class StopListPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.user.is_client:
            return False
        if request.method == "GET" and any([
            check_role_employee(request.user, Employee.Roles.COOK),
            check_role_employee(request.user, Employee.Roles.WAITER),
        ]):
            return True
        if request.method == "POST":
            return check_role_employee(request.user, Employee.Roles.COOK)
        return check_role_employee(request.user, Employee.Roles.COOK)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "DELETE":
            return check_role_employee(request.user, Employee.Roles.COOK)


class OrderAndDishesPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.user.is_client:
            return False
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PATCH", "PUT"):
            return any([
                check_role_employee(request.user, Employee.Roles.COOK),
                check_role_employee(request.user, Employee.Roles.CHEF),
                check_role_employee(request.user, Employee.Roles.SOUS_CHEF),
                check_role_employee(request.user, Employee.Roles.WAITER),
            ])
        if request.method == "DELETE":
            return check_role_employee(request.user, Employee.Roles.WAITER)

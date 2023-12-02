from rest_framework import permissions


class CategoryPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.method == "GET"

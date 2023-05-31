from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_authenticated


# class IsDriver(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_driver:
#             return True
#         return PermissionError

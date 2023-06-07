from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_authenticated


class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_driver = getattr(request.user, 'is_driver', None)
        if is_driver:
            return True

        return False


# class IsDriver(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_driver:
#             return True
#         return PermissionError

from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            raise NotAuthenticated("You need to be logged in to perform this action")

        SAFE_METHODS = ("HEAD", "OPTIONS")
        if request.method in SAFE_METHODS:
            return request.user.user_type == "admin"
        return request.user.user_type == "admin"

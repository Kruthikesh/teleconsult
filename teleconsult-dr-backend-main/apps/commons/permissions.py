from rest_framework import permissions
from apps.commons.constants import UserTypes


class GetMethodPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        request_method = request.method
        if request_method == 'GET':
            return True

        return False


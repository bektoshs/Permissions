from rest_framework.permissions import BasePermission


class IsSuperPermission(BasePermission):
    """
    Allows access only to admin users.
    """
    ROLE_NAME = 'superadmin'

    def has_permission(self, request, view):
        if request.user and request.user.group.filter(name=self.ROLE_NAME):
            return True
        return False


class IsReadOnlyPermission(BasePermission):
    ROLE_NAME = 'read_only'

    def has_permission(self, request, view):
        if request.user and request.user.group.filter(name=self.ROLE_NAME):
            return True
        return False


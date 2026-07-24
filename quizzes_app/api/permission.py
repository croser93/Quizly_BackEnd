from rest_framework.permissions import BasePermission

class UserIsCreatorOrAdmin(BasePermission):
    """
    Custom permission to only allow the quiz creator and admins access.

    Users are granted access if they are either:
    - Superuser  = GET, PATCH, DELETE
    - Owner      = GET, PATCH, DELETE
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'PATCH', 'DELETE'):
            return bool(request.user and (request.user.is_superuser or request.user == obj.user))

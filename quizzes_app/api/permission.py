from rest_framework.permissions import BasePermission


class UserIsCreatorOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method =='GET':
            return bool(request.user and (request.user.is_superuser or request.user == obj.user))
        elif request.method =='PATCH':
            return bool(request.user and (request.user.is_superuser or request.user == obj.user))
        elif request.method =='DELETE':
            return bool(request.user and request.user.is_superuser)
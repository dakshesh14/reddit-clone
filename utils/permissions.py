from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # FIXME: This is throw error when checking permission for Community
        return obj.owner == request.user or obj.community.owner == request.user or request.user.is_superuser


class IsCommunityOwnerOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.community.owner == request.user or request.user.is_superuser

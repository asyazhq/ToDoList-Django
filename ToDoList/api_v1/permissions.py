from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only the owner of a task can edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False 

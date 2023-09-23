from rest_framework import permissions

class DisallowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        return False
    
    def has_object_permission(self, request, view, obj):
        return False
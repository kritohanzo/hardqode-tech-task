from rest_framework import permissions


class DisallowAny(permissions.BasePermission):
    """Пермишен для запрета любых запросов. Установлен по умолчанию."""

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False

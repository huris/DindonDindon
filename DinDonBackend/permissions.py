from rest_framework import permissions

from Users.models import UserType


class SuperPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == UserType.Manager or request.user.is_superuser


class UserBasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class CustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == UserType.Customer


class ChefPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == UserType.Chef


class WaiterPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == UserType.Waiter

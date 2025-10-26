# users/permissions.py
from rest_framework import permissions
from .models import Customer, Admin, Auditor

class IsCustomerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'admin')

class IsAuditorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'auditor')

class IsAuditorOwnerOrAdmin(permissions.BasePermission):
    """
    Admins can view all auditors.
    Auditors can view only their own profile.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'admin'):
            return True  # Admin can see all
        elif hasattr(request.user, 'auditor'):
            return obj.user == request.user  # Auditor sees only self
        return False
class IsAdminUserPermission(permissions.BasePermission):
    """
    Only admins can access.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'admin')  # Only if Admin profile exists
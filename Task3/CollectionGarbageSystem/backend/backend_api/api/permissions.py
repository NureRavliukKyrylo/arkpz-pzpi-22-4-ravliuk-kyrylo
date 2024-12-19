from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from ..middleware import get_user_from_token

# Permissions for role-based access control and user authentication.

class IsAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
        try:
            get_user_from_token(request)
            return True
        except AuthenticationFailed:
            return False


class RoleBasedPermission(BasePermission):
    
    required_roles = []

    def has_permission(self, request, view):
        user = get_user_from_token(request)
        if not self.required_roles or user.role.name in self.required_roles:
            return True
        raise PermissionDenied('You do not have the required permissions to access this resource.')


class IsAdminAuthenticated(RoleBasedPermission):
    
    required_roles = ['Admin']


class IsAdminOrOperatorAuthenticated(RoleBasedPermission):
    
    required_roles = ['Admin', 'Operator']


class IsUserAuthenticated(RoleBasedPermission):
    
    required_roles = ['Customer']

class IsAdminOrOperatorOrUserAuthenticated(RoleBasedPermission):
    
    required_roles = ['Admin', 'Operator', 'Customer']

class IsAdminOrUserAutheticated(RoleBasedPermission):
    
    required_roles = ['Admin', 'Customer']
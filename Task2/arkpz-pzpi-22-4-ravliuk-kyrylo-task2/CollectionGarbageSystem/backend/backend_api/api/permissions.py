from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import jwt
from django.conf import settings
from ..models import CustomUser

# Permissions for role-based access control and user authentication.
class JWTAuthenticationHelper:
    
    @staticmethod
    def get_user_from_token(request):
        token = request.COOKIES.get('access_token')
        if not token:
            raise AuthenticationFailed('User is not authenticated. Token not found.')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

        user_id = payload.get('user_id')
        if not user_id:
            raise AuthenticationFailed('User ID not found in the token.')

        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            raise AuthenticationFailed('User not found.')

        return user


class IsAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
        try:
            JWTAuthenticationHelper.get_user_from_token(request)
            return True
        except AuthenticationFailed:
            return False


class RoleBasedPermission(BasePermission):
    
    required_roles = []

    def has_permission(self, request, view):
        user = JWTAuthenticationHelper.get_user_from_token(request)
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
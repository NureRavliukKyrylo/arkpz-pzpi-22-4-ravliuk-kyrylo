from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from ..models import CustomUser

def get_user_from_jwt(request):
    token = request.COOKIES.get('access_token')
    if not token:
        raise AuthenticationFailed('Token not found in cookies')

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')

    user_id = payload.get('user_id')
    if not user_id:
        raise AuthenticationFailed('User ID not found in the token')

    user = CustomUser.objects.filter(id=user_id).first()
    if not user:
        raise AuthenticationFailed('User not found')

    if user.role.name != 'Admin':  
        raise AuthenticationFailed('User does not have Admin privileges')

    return user 
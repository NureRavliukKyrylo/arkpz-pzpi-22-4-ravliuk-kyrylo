import jwt
from threading import local
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser 
from django.utils.functional import SimpleLazyObject

# Thread-local storage to hold the request object, ensuring request data is isolated per thread
_request_storage = local()

# Function to get the current request from thread-local storage
def get_current_request():
    return getattr(_request_storage, 'request', None)

# Function to extract the user from the token in the request
def get_user_from_token(request):
    if request is None:
        raise AuthenticationFailed('No request object available.')

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

# Function to get the user from the request, caching the result for subsequent access
def get_user(request):
    if not request:
        return None
    
    if not hasattr(request, '_cached_user'):
        try:
            request._cached_user = get_user_from_token(request)
        except AuthenticationFailed:
            request._cached_user = None
    return request._cached_user

# Middleware class to manage request and user access
class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_storage.request = request
        
        request.user = SimpleLazyObject(lambda: get_user(request))

        response = self.get_response(request)

        _request_storage.request = None 
        return response

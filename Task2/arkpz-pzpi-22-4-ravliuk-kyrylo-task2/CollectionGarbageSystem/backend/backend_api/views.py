from django.http import JsonResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from backend_api.api.serializers import MyTokenObtainPairSerializer,RegisterCustomerSerializer,LoginCustomerSerializer,DateRangeSerializer
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status

# View to register a new customer
class RegisterCustomerView(APIView):
    @swagger_auto_schema(
        request_body=RegisterCustomerSerializer,
        responses={
            201: 'User registered successfully',
            400: 'Invalid input',
        }
    )
    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to login an existing customer
class LoginCustomerView(APIView):
    @swagger_auto_schema(
        request_body=LoginCustomerSerializer,
        responses={
            200: 'Login successful',
            400: 'Invalid login credentials',
            500: 'An error occurred',
        }
    )
    def post(self, request):
        serializer = LoginCustomerSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                user = CustomUser.objects.get(username=username)

                if not check_password(password, user.password):
                    raise AuthenticationFailed('Invalid login credentials')

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response = Response({
                    'message': 'Login successful',
                }, status=200)

                response.set_cookie('access_token', access_token, httponly=True, secure=True, max_age=3600, path='/')
                response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, max_age=86400, path='/')

                return response
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed('Invalid login credentials')
        return Response(serializer.errors, status=400)


class MineTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# View to logout a customer
class LogoutCustomerView(APIView):

    @swagger_auto_schema(
            operation_description="Logs out the user by deleting the access and refresh tokens from the cookies.",
            responses={
                200: openapi.Response(
                    description="Logout successful",
                    schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Logout successful')
                    })
                ),
                403: 'Permission denied - User must be authenticated.',
                500: 'Unexpected error occurred'
            }
        )
    def post(self, request):
        try:
            response = JsonResponse({'message': 'Logout successful'}, status=200)
            
            response.delete_cookie('access_token', path='/')
            response.delete_cookie('refresh_token', path='/')

            return response
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


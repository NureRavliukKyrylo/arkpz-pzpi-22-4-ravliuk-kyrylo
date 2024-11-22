from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework_simplejwt.tokens import RefreshToken
import json
from rest_framework_simplejwt.views import TokenObtainPairView
from backend_api.api.serializers import MyTokenObtainPairSerializer
from .models import CustomUser
from django.contrib.auth.hashers import check_password

@csrf_exempt
def registerCustomer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')  
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return JsonResponse({"error": "Please provide all required fields."}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email is already in use."}, status=400)

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username is already in use."}, status=400)

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({"message": "User registered successfully."}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed."}, status=400)

@csrf_exempt
def loginCustomer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            try:
                user = CustomUser.objects.get(username=username)

                if check_password(password, user.password):

                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)

                    return JsonResponse({
                        'access': access_token,
                        'refresh': refresh_token,
                        'is_admin': user.is_superuser
                    }, status=200)
                else:
                    return JsonResponse({'error': 'Invalid login credentials'}, status=400)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Invalid login credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)

class MineTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@csrf_exempt
def logoutCustomer(request):
    auth_logout(request)
    return JsonResponse({'message': 'Logout successful'}, status=200)

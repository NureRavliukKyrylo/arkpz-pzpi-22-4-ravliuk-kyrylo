from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework_simplejwt.tokens import RefreshToken
import json
from rest_framework_simplejwt.views import TokenObtainPairView
from backend_api.api.serializers import MyTokenObtainPairSerializer,RegisterCustomerSerializer,LoginCustomerSerializer,DateRangeSerializer
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from .models import WasteHistory
from backend_api.api.validators import validate_date_range
from backend_api.api.pdf_generators import generate_waste_report_pdf,generate_waste_report_for_containers_pdf
from django.http import JsonResponse
from .models import IoTFillingContainer
from backend_api.api.jwt_guard import get_user_from_jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import AuthenticationFailed

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

class GetReportOfStationsView(APIView):
    @swagger_auto_schema(
        request_body=DateRangeSerializer,
        responses={
            200: 'PDF report generated successfully',
            400: 'Invalid input',
            403: 'Permission denied',
            500: 'Unexpected error'
        }
    )
    def post(self, request):
        try:
            user = get_user_from_jwt(request)
            print(user)
            data = request.data
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            if not start_date or not end_date:
                return JsonResponse({"error": "Both start_date and end_date are required."}, status=400)

            waste_histories = WasteHistory.objects.filter(
                recycling_date__gte=start_date,
                recycling_date__lte=end_date
            )

            response = generate_waste_report_pdf(waste_histories, start_date, end_date)
            return response

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except PermissionDenied as e:
            return JsonResponse({"error": str(e)}, status=403)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    
class GetReportOfStationsView(APIView):

    @swagger_auto_schema(
        request_body=DateRangeSerializer,
        responses={
            200: 'PDF report generated successfully',
            400: 'Invalid input',
            403: 'Permission denied',
            500: 'Unexpected error'
        }
    )
    def post(self, request):

        try:
            user = get_user_from_jwt(request)
            print(f"User: {user}")

            data = request.data
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not start_date or not end_date:
                return JsonResponse({"error": "Both start_date and end_date are required."}, status=400)

            start_date, end_date = validate_date_range({'start_date': start_date, 'end_date': end_date})

            waste_histories = WasteHistory.objects.filter(
                recycling_date__gte=start_date,
                recycling_date__lte=end_date
            )

            if waste_histories.exists():
                response = generate_waste_report_pdf(waste_histories, start_date, end_date)
                return response

            waste_histories = IoTFillingContainer.objects.filter(
                time_of_detect__gte=start_date,
                time_of_detect__lte=end_date
            ).select_related('container_id_filling__type_of_container_id')

            if waste_histories.exists():
                response = generate_waste_report_for_containers_pdf(waste_histories, start_date, end_date)
                return response

            return JsonResponse({"error": "No data found for the given date range."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except PermissionDenied:
            return JsonResponse({"error": "Permission denied"}, status=403)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
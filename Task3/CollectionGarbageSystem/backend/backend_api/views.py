from django.http import HttpResponse,JsonResponse
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
from backend_api.api.permissions import IsAdminAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import json
from django.apps import apps
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import pre_delete, post_delete
from contextlib import contextmanager
from django.db import connection
from datetime import datetime

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
    permission_classes = [IsAdminAuthenticated]
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
            data = request.data
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            if not start_date or not end_date:
                return JsonResponse({"error": "Both start_date and end_date are required."}, status=400)

            waste_histories = WasteHistory.objects.filter(
                recycling_date__gte=start_date,
                recycling_date__lte=end_date,
                station_id__isnull=False
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

    
class GetReportOfContainersView(APIView):
    permission_classes = [IsAdminAuthenticated]
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
            data = request.data
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not start_date or not end_date:
                return JsonResponse({"error": "Both start_date and end_date are required."}, status=400)

            start_date, end_date = validate_date_range({'start_date': start_date, 'end_date': end_date})

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

def custom_json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  
    raise TypeError(f"Type {type(obj)} not serializable")

class DownloadBackupView(APIView):
    @swagger_auto_schema(
        operation_summary="Download database backup",
        operation_description=(
            "This endpoint generates a JSON backup of the specified models' data in the database. "
            "The response will be a downloadable JSON file."
        ),
        responses={
            200: openapi.Response(
                description="Backup file generated successfully",
                examples={
                    "application/json": {
                        "message": "JSON file downloaded successfully."
                    }
                }
            ),
            404: openapi.Response(
                description="No data available for backup.",
                examples={
                    "application/json": {
                        "message": "No data available for backup."
                    }
                }
            ),
            500: openapi.Response(
                description="Unexpected error",
                examples={
                    "application/json": {
                        "error": "An error occurred: <error message>"
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        models_to_load = [  
            "backend_api.roleuser",
            "backend_api.StationOfContainersStatus",
            "backend_api.NotificationTypes",
            "backend_api.StatusOfContainer",
            "backend_api.TypeOfContainer",
            "backend_api.customuser",
            "backend_api.StationOfContainers",
            "backend_api.CollectionSchedules",
            "backend_api.NotificationsUser",
            "backend_api.Containers",
            "backend_api.IoTFillingContainer",
            "backend_api.WasteHistory",
            "backend_api.AdminLoggingChanges",
        ]
        
        try:
            backup_data = {}

            for model_path in models_to_load:
                if "." not in model_path:
                    backup_data[model_path] = "Invalid model format. Expected '<app_label>.<model_name>'."
                    continue

                try:
                    app_label, model_name = model_path.split(".")
                    model = apps.get_model(app_label, model_name)
                    model_data = list(model.objects.all().values())  
                    backup_data[model_path] = model_data
                except LookupError:
                    backup_data[model_path] = f"Model {model_path} not found."

            if not any(isinstance(v, list) and v for v in backup_data.values()):
                return Response({"message": "No data available for backup."}, status=status.HTTP_404_NOT_FOUND)

            json_data = json.dumps(backup_data, default=custom_json_serializer, indent=4)

            response = HttpResponse(json_data, content_type="application/json")
            response['Content-Disposition'] = 'attachment; filename="models_backup.json"'
            return response

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

@contextmanager
def disable_all_signals():
    signals_to_disconnect = [pre_save, post_save, pre_delete, post_delete]
    disconnected_signals = {}

    for signal in signals_to_disconnect:
        disconnected_signals[signal] = signal.receivers[:]
        signal.receivers.clear()

    try:
        yield
    finally:
        for signal, receivers in disconnected_signals.items():
            signal.receivers.extend(receivers)

class RestoreBackupView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="Restore database backup",
        operation_description="Restores data to the database from a JSON backup file. The file should be in the same format as the backup data.",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="JSON backup file to restore data"
            )
        ],
        responses={
            200: openapi.Response(
                description="Data restored successfully",
                examples={
                    "application/json": {
                        "message": "Data restored successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid backup data",
                examples={
                    "application/json": {
                        "error": "Invalid data format."
                    }
                }
            ),
            500: openapi.Response(
                description="Unexpected error",
                examples={
                    "application/json": {
                        "error": "An error occurred: <error message>"
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({"error": "No file provided."}, status=400)

        try:
            backup_data = json.load(file)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

        with disable_all_signals():
            try:
                errors = []
                for model_path, records in backup_data.items():
                    if not isinstance(records, list):
                        errors.append(f"Data for {model_path} is not a list.")
                        continue

                    try:
                        app_label, model_name = model_path.split(".")
                        model = apps.get_model(app_label, model_name)
                    except (ValueError, LookupError):
                        errors.append(f"Invalid model path: {model_path}")
                        continue

                    with transaction.atomic():
                        for record in records:
                            try:
                                obj, created = model.objects.update_or_create(
                                    id=record.get("id"), defaults=record
                                )
                            except IntegrityError as e:
                                errors.append(
                                    f"Integrity error for {model_path} with ID {record.get('id')}: {str(e)}"
                                )
                                continue

                        self.update_sequence_for_model(model)

                if errors:
                    return JsonResponse({"message": "Partial restore completed.", "errors": errors}, status=400)

                return JsonResponse({"message": "Data restored successfully."}, status=200)

            except Exception as e:
                return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    def update_sequence_for_model(self, model):
        table_name = model._meta.db_table
        pk_name = model._meta.pk.column

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT MAX({pk_name}) FROM {table_name}")
            max_id = cursor.fetchone()[0] or 0

            sequence_name = f"{table_name}_{pk_name}_seq"
            cursor.execute(f"SELECT setval('{sequence_name}', %s)", [max_id + 1])
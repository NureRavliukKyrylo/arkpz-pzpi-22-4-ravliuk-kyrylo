from django.http import JsonResponse
import json
from backend_api.api.serializers import DateRangeSerializer
from ...models import WasteHistory,IoTFillingContainer
from backend_api.api.validators import validate_date_range
from backend_api.api.pdf_generators import generate_waste_report_pdf,generate_waste_report_for_containers_pdf
from backend_api.api.permissions import IsAdminAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied

class GetReportOfStationsView(APIView):
    # Define permission classes, only admin users can access this view
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
            # Extract data from the request body
            data = request.data
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            if not start_date or not end_date:
                return JsonResponse({"error": "Both start_date and end_date are required."}, status=400)

            # Filter the WasteHistory objects based on the provided date range
            waste_histories = WasteHistory.objects.filter(
                recycling_date__gte=start_date,
                recycling_date__lte=end_date,
                station_id__isnull=False
            )

             # Generate the PDF report for waste histories
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
     # Define permission classes, only admin users can access this view
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
         # Extract data from the request body
        try:
            data = request.data
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not start_date or not end_date:
                return JsonResponse({"error": "Both start_date and end_date are required."}, status=400)

            start_date, end_date = validate_date_range({'start_date': start_date, 'end_date': end_date})

            # Filter the IoTFillingContainer objects based on the provided date range
            waste_histories = IoTFillingContainer.objects.filter(
                time_of_detect__gte=start_date,
                time_of_detect__lte=end_date
            ).select_related('container_id_filling__type_of_container_id')

            # If data is found, generate the PDF report for containers
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
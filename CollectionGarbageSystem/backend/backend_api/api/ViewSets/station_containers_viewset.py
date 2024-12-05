from backend_api.api.ViewSets.base_viewset import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from backend_api.api.permissions import IsAdminAuthenticated,IsAdminOrOperatorOrUserAuthenticated
from ..serializers import StationOfContainersSerializer,UpdateStationStatusSerializer
from ...models import StationOfContainers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi

class StationOfContainersViewSet(GenericViewSet):
    queryset = StationOfContainers.objects.all()
    serializer_class = StationOfContainersSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status_station__station_status_name'] 
    search_fields = ['station_of_containers_name']

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAdminOrOperatorOrUserAuthenticated]
        else:
            permission_classes = [IsAdminAuthenticated]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_description="Create a new Station",
        request_body=StationOfContainersSerializer,
        responses={201: StationOfContainersSerializer}
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="List all Stations with filtering and search options",
        manual_parameters=[
            openapi.Parameter(
                'status_station__station_status_name',
                openapi.IN_QUERY,
                description="Filter stations by status name (e.g., 'Active')",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search stations by name",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: StationOfContainersSerializer(many=True)}
    )
    def list(self, request):
        queryset = self.queryset

        queryset = self.apply_filters(request, queryset)

        queryset = self.apply_search(request, queryset)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def apply_filters(self, request, queryset):
        filter_backend = DjangoFilterBackend()
        return filter_backend.filter_queryset(request, queryset, self)

    def apply_search(self, request, queryset):
        search_backend = SearchFilter()
        return search_backend.filter_queryset(request, queryset, self)
    
    @action(detail=True, methods=['patch'],url_path='update-status')
    @swagger_auto_schema(
        operation_description="Partially update the status_station field of a station",
        request_body=UpdateStationStatusSerializer,
        responses={200: StationOfContainersSerializer}
    )
    def update_status(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = UpdateStationStatusSerializer(instance, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(StationOfContainersSerializer(instance).data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except StationOfContainers.DoesNotExist:
            return Response({"error": f"A Station with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_description="Update a Station",
        request_body=StationOfContainersSerializer,
        responses={201: StationOfContainersSerializer}
    )
    def update(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.model.DoesNotExist:
            return Response({"error": f"A Station with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)
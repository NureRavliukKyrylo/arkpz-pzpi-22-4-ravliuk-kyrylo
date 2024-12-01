from backend_api.api.ViewSets.base_viewset import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from backend_api.api.permissions import IsAdminAuthenticated,IsAdminOrOperatorAuthenticated
from ..serializers import ContainersSerializer
from ...models import Containers
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi

class ContainersViewSet(GenericViewSet):
    queryset = Containers.objects.all()
    serializer_class = ContainersSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['status_container_id__status_name', 'type_of_container_id__type_name_container']
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAdminOrOperatorAuthenticated]
        else:
            permission_classes = [IsAdminAuthenticated]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_description="Create a new Container",
        request_body=ContainersSerializer,
        responses={201: ContainersSerializer}
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="List all Containers with filtering options",
        manual_parameters=[
            openapi.Parameter(
                'status_container_id__status_name',
                openapi.IN_QUERY,
                description="Filter containers by status name (e.g., 'Active')",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'type_of_container_id__type_name_container',
                openapi.IN_QUERY,
                description="Filter containers by type name (e.g., 'Plastic')",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: ContainersSerializer(many=True)}
    )
    def list(self, request):
        queryset = self.queryset

        queryset = self.apply_filters(request, queryset)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def apply_filters(self, request, queryset):
        filter_backend = DjangoFilterBackend()
        return filter_backend.filter_queryset(request, queryset, self)
    
    @swagger_auto_schema(
        operation_description="Update container",
        request_body=ContainersSerializer,
        responses={201: ContainersSerializer}
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
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
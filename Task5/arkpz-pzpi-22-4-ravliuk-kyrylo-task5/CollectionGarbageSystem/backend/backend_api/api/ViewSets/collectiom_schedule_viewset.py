from rest_framework.exceptions import ValidationError
from backend_api.api.ViewSets.base_viewset import GenericViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from backend_api.api.permissions import IsAdminAuthenticated, IsAdminOrOperatorOrUserAuthenticated
from ..serializers import CollectionSchedulesSerializer, CollectionScheduleUpdateDateSerializer
from ...models import CollectionSchedules, StationOfContainers
from rest_framework import status
from rest_framework.decorators import action

class CollectionSchedulesViewSet(GenericViewSet):
    queryset = CollectionSchedules.objects.all()
    serializer_class = CollectionSchedulesSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAdminOrOperatorOrUserAuthenticated]
        else:
            permission_classes = [IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        operation_description="Create a new Collection Schedule",
        request_body=CollectionSchedulesSerializer,
        responses={201: CollectionSchedulesSerializer}
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a Collection Schedule",
        request_body=CollectionSchedulesSerializer,
        responses={201: CollectionSchedulesSerializer}
    )
    def update(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
        except self.queryset.model.DoesNotExist:
            raise ValidationError({"error": f"A Collection schedule with ID {pk} does not exist."})

        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

# Custom action to update the collection date for a specific collection schedule
    @action(detail=True, methods=['patch'], url_path='update-collection-date')
    @swagger_auto_schema(
        operation_description="Update collection date for station",
        request_body=CollectionScheduleUpdateDateSerializer,
        responses={200: CollectionSchedulesSerializer}
    )
    def sensor_value_change(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
        except CollectionSchedules.DoesNotExist:
            raise ValidationError({"error": f"A Collection schedule with ID {pk} does not exist."})

        serializer = CollectionScheduleUpdateDateSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

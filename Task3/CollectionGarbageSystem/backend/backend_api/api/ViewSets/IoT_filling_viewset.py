from backend_api.api.ViewSets.base_viewset import GenericViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from backend_api.api.permissions import IsAdminAuthenticated
from ..serializers import IoTFillingContainerSerializer,SensorValueUpdateSerializer
from ...models import IoTFillingContainer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class IoTFillingContainerViewSet(GenericViewSet):
    queryset = IoTFillingContainer.objects.all()
    serializer_class = IoTFillingContainerSerializer

    def get_permissions(self):
        permission_classes = [IsAdminAuthenticated]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_description="Create a new Filling level",
        request_body=IoTFillingContainerSerializer,
        responses={201: IoTFillingContainerSerializer}
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Update a new Filling level",
        request_body=IoTFillingContainerSerializer,
        responses={201: IoTFillingContainerSerializer}
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
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)\
    
    @action(detail=True, methods=['patch'], url_path='sensor-value-update')
    @swagger_auto_schema(
        operation_description="Update sensor value of a filling container (partial update, only 'sensor_value' field allowed)",
        request_body=SensorValueUpdateSerializer,
        responses={200: IoTFillingContainerSerializer}
    )
    def sensor_value_change(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
        except IoTFillingContainer.DoesNotExist:
            return Response({"error": f"A Filling sensor with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SensorValueUpdateSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(IoTFillingContainerSerializer(instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
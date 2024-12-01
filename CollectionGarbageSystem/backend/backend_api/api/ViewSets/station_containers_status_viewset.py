from backend_api.api.ViewSets.base_viewset import GenericViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from backend_api.api.permissions import IsAdminAuthenticated
from ..serializers import StationOfContainersStatusSerializer
from ...models import StationOfContainersStatus
from rest_framework.response import Response
from rest_framework import status

class StationOfContainersStatusViewSet(GenericViewSet):
    queryset = StationOfContainersStatus.objects.all()
    serializer_class = StationOfContainersStatusSerializer
    

    def get_permissions(self):
        permission_classes = [IsAdminAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        operation_description="Create a new Station Status",
        request_body=StationOfContainersStatusSerializer,
        responses={201: StationOfContainersStatusSerializer}
        )
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Update a Station Status",
        request_body=StationOfContainersStatusSerializer,
        responses={201: StationOfContainersStatusSerializer}
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
from backend_api.api.ViewSets.base_viewset import GenericViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from backend_api.api.permissions import IsAdminAuthenticated,IsAdminOrOperatorOrUserAuthenticated
from ..serializers import CollectionSchedulesSerializer
from ...models import CollectionSchedules
from rest_framework.response import Response
from rest_framework import status

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
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
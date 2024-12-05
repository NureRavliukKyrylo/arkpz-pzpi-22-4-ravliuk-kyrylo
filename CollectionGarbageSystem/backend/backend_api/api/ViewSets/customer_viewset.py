from backend_api.api.ViewSets.base_viewset import GenericViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from backend_api.api.permissions import IsAdminAuthenticated,IsUserAuthenticated
from ..serializers import CustomerSerializer,PasswordUpdateSerializer,CustomerUpdateSerializer
from ...models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class CustomerViewSet(GenericViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomerSerializer
    
    def get_permissions(self):
        if self.action == 'partial_update':
            permission_classes = [IsUserAuthenticated]
        else:
            permission_classes = [IsAdminAuthenticated]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_description="Create a new customer",
        request_body=CustomerSerializer,
        responses={201: CustomerSerializer}
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
    operation_description="Update a customer without modifying the password",
    request_body=CustomerUpdateSerializer,
    responses={200: CustomerSerializer}
    )
    def update(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.model.DoesNotExist:
            return Response({"error": f"A Customer with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['patch'], url_path='change-password')
    @swagger_auto_schema(
        operation_description="Change password for a customer",
        request_body=PasswordUpdateSerializer,
        responses={200: "Password updated successfully", 400: "Invalid input"}
    )
    def change_password(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = PasswordUpdateSerializer(
                data=request.data,
                context={'user': instance}
            )
            if serializer.is_valid():
                serializer.update(instance, serializer.validated_data)
                return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.model.DoesNotExist:
            return Response({"error": f"A Customer with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from backend_api.models import (
    CustomUser, RoleUser, StationOfContainersStatus, StationOfContainers,
    CollectionSchedules, NotificationTypes, NotificationsUser, StatusOfContainer,
    TypeOfContainer, Containers, IoTFillingContainer, WasteHistory
)
from .serializers import (
    CustomerSerializer, RoleUserSerializer, StationOfContainersStatusSerializer,
    StationOfContainersSerializer, CollectionSchedulesSerializer, NotificationTypesSerializer,
    NotificationsUserSerializer, StatusOfContainerSerializer, TypeOfContainerSerializer,
    ContainersSerializer, IoTFillingContainerSerializer, WasteHistorySerializer
)

from drf_yasg.utils import swagger_auto_schema

class GenericViewSet(viewsets.ViewSet):
    queryset = None
    serializer_class = None

    def format_error(self, errors):
        error_messages = []
        
        for field, msgs in errors.items():
            if isinstance(msgs, list):
                for msg in msgs:
                    error_messages.append(f"{msg}")
            else:
                error_messages.append(f"{msgs}")
        
        return {"error": error_messages}
    
    def list(self, request):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        except self.queryset.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

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

    def partial_update(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except self.queryset.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


class CustomerViewSet(GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomerSerializer

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

class RoleUserViewSet(GenericViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleUserSerializer

    @swagger_auto_schema(
        operation_description="Create a new Role",
        request_body=RoleUserSerializer,
        responses={201: RoleUserSerializer}
    )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
class StationOfContainersStatusViewSet(GenericViewSet):
    queryset = StationOfContainersStatus.objects.all()
    serializer_class = StationOfContainersStatusSerializer

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

class StationOfContainersViewSet(GenericViewSet):
    queryset = StationOfContainers.objects.all()
    serializer_class = StationOfContainersSerializer

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

class CollectionSchedulesViewSet(GenericViewSet):
    queryset = CollectionSchedules.objects.all()
    serializer_class = CollectionSchedulesSerializer

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

class NotificationTypesViewSet(GenericViewSet):
    queryset = NotificationTypes.objects.all()
    serializer_class = NotificationTypesSerializer

    @swagger_auto_schema(
        operation_description="Create a new Notification Type",
        request_body=NotificationTypesSerializer,
        responses={201: NotificationTypesSerializer}
    )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class NotificationsUserViewSet(GenericViewSet):
    queryset = NotificationsUser.objects.all()
    serializer_class = NotificationsUserSerializer

    @swagger_auto_schema(
        operation_description="Create a new Notifications",
        request_body=NotificationsUserSerializer,
        responses={201: NotificationsUserSerializer}
    )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class StatusOfContainerViewSet(GenericViewSet):
    queryset = StatusOfContainer.objects.all()
    serializer_class = StatusOfContainerSerializer

    @swagger_auto_schema(
        operation_description="Create a new Status of Container",
        request_body=StatusOfContainerSerializer,
        responses={201: StatusOfContainerSerializer}
    )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class TypeOfContainerViewSet(GenericViewSet):
    queryset = TypeOfContainer.objects.all()
    serializer_class = TypeOfContainerSerializer

    @swagger_auto_schema(
        operation_description="Create a new Type of Container",
        request_body=TypeOfContainerSerializer,
        responses={201: TypeOfContainerSerializer}
    )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class ContainersViewSet(GenericViewSet):
    queryset = Containers.objects.all()
    serializer_class = ContainersSerializer

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

class IoTFillingContainerViewSet(GenericViewSet):
    queryset = IoTFillingContainer.objects.all()
    serializer_class = IoTFillingContainerSerializer

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

class WasteHistoryViewSet(GenericViewSet):
    queryset = WasteHistory.objects.all()
    serializer_class = WasteHistorySerializer

    @swagger_auto_schema(
        operation_description="Create a new Waste History",
        request_body=WasteHistorySerializer,
        responses={201: WasteHistorySerializer}
    )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


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

class GenericViewSet(viewsets.ViewSet):
    queryset = None
    serializer_class = None

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.queryset.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

class RoleUserViewSet(GenericViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleUserSerializer

class StationOfContainersStatusViewSet(GenericViewSet):
    queryset = StationOfContainersStatus.objects.all()
    serializer_class = StationOfContainersStatusSerializer

class StationOfContainersViewSet(GenericViewSet):
    queryset = StationOfContainers.objects.all()
    serializer_class = StationOfContainersSerializer

class CollectionSchedulesViewSet(GenericViewSet):
    queryset = CollectionSchedules.objects.all()
    serializer_class = CollectionSchedulesSerializer

class NotificationTypesViewSet(GenericViewSet):
    queryset = NotificationTypes.objects.all()
    serializer_class = NotificationTypesSerializer

class NotificationsUserViewSet(GenericViewSet):
    queryset = NotificationsUser.objects.all()
    serializer_class = NotificationsUserSerializer

class StatusOfContainerViewSet(GenericViewSet):
    queryset = StatusOfContainer.objects.all()
    serializer_class = StatusOfContainerSerializer

class TypeOfContainerViewSet(GenericViewSet):
    queryset = TypeOfContainer.objects.all()
    serializer_class = TypeOfContainerSerializer

class ContainersViewSet(GenericViewSet):
    queryset = Containers.objects.all()
    serializer_class = ContainersSerializer

class IoTFillingContainerViewSet(GenericViewSet):
    queryset = IoTFillingContainer.objects.all()
    serializer_class = IoTFillingContainerSerializer

class WasteHistoryViewSet(GenericViewSet):
    queryset = WasteHistory.objects.all()
    serializer_class = WasteHistorySerializer

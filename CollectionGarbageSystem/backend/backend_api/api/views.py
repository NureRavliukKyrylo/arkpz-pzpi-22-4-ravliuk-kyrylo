from rest_framework import viewsets
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

# ViewSet for CustomUser
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomerSerializer

# ViewSet for RoleUser
class RoleUserViewSet(viewsets.ModelViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleUserSerializer

# ViewSet for StationOfContainersStatus
class StationOfContainersStatusViewSet(viewsets.ModelViewSet):
    queryset = StationOfContainersStatus.objects.all()
    serializer_class = StationOfContainersStatusSerializer

# ViewSet for StationOfContainers
class StationOfContainersViewSet(viewsets.ModelViewSet):
    queryset = StationOfContainers.objects.all()
    serializer_class = StationOfContainersSerializer

# ViewSet for CollectionSchedules
class CollectionSchedulesViewSet(viewsets.ModelViewSet):
    queryset = CollectionSchedules.objects.all()
    serializer_class = CollectionSchedulesSerializer

# ViewSet for NotificationTypes
class NotificationTypesViewSet(viewsets.ModelViewSet):
    queryset = NotificationTypes.objects.all()
    serializer_class = NotificationTypesSerializer

# ViewSet for NotificationsUser
class NotificationsUserViewSet(viewsets.ModelViewSet):
    queryset = NotificationsUser.objects.all()
    serializer_class = NotificationsUserSerializer

# ViewSet for StatusOfContainer
class StatusOfContainerViewSet(viewsets.ModelViewSet):
    queryset = StatusOfContainer.objects.all()
    serializer_class = StatusOfContainerSerializer

# ViewSet for TypeOfContainer
class TypeOfContainerViewSet(viewsets.ModelViewSet):
    queryset = TypeOfContainer.objects.all()
    serializer_class = TypeOfContainerSerializer

# ViewSet for Containers
class ContainersViewSet(viewsets.ModelViewSet):
    queryset = Containers.objects.all()
    serializer_class = ContainersSerializer

# ViewSet for IoTFillingContainer
class IoTFillingContainerViewSet(viewsets.ModelViewSet):
    queryset = IoTFillingContainer.objects.all()
    serializer_class = IoTFillingContainerSerializer

# ViewSet for WasteHistory
class WasteHistoryViewSet(viewsets.ModelViewSet):
    queryset = WasteHistory.objects.all()
    serializer_class = WasteHistorySerializer

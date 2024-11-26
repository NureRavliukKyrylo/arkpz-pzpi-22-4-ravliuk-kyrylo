from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, RoleUserViewSet, StationOfContainersStatusViewSet,
    StationOfContainersViewSet, CollectionSchedulesViewSet, NotificationTypesViewSet,
    NotificationsUserViewSet, StatusOfContainerViewSet, TypeOfContainerViewSet,
    ContainersViewSet, IoTFillingContainerViewSet, WasteHistoryViewSet
)

ROUTE_VIEWSET_MAPPING = {
    'customers': CustomerViewSet,
    'roleUsers': RoleUserViewSet,
    'stationOfContainersStatuses': StationOfContainersStatusViewSet,
    'stationOfContainers': StationOfContainersViewSet,
    'collectionSchedules': CollectionSchedulesViewSet,
    'notificationTypes': NotificationTypesViewSet,
    'notificationsUsers': NotificationsUserViewSet,
    'statusOfContainers': StatusOfContainerViewSet,
    'typeOfContainers': TypeOfContainerViewSet,
    'containers': ContainersViewSet,
    'iotFillingContainers': IoTFillingContainerViewSet,
    'wasteHistories': WasteHistoryViewSet,
}

router = DefaultRouter()

for route, viewset in ROUTE_VIEWSET_MAPPING.items():
    router.register(route, viewset)

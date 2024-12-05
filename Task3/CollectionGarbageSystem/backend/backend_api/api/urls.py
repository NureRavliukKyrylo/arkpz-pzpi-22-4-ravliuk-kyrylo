from rest_framework.routers import DefaultRouter
from backend_api.api.ViewSets.customer_viewset import CustomerViewSet
from backend_api.api.ViewSets.role_user_viewset import RoleUserViewSet
from backend_api.api.ViewSets.station_containers_status_viewset import StationOfContainersStatusViewSet 
from backend_api.api.ViewSets.station_containers_viewset import StationOfContainersViewSet
from backend_api.api.ViewSets.collectiom_schedule_viewset import CollectionSchedulesViewSet
from backend_api.api.ViewSets.notification_types_viewset import NotificationTypesViewSet
from backend_api.api.ViewSets.notifications_viewset import NotificationsUserViewSet
from backend_api.api.ViewSets.status_container_viewset import StatusOfContainerViewSet
from backend_api.api.ViewSets.type_container_viewset import TypeOfContainerViewSet
from backend_api.api.ViewSets.containers_viewset import ContainersViewSet
from backend_api.api.ViewSets.IoT_filling_viewset import IoTFillingContainerViewSet
from backend_api.api.ViewSets.histories_viewset import WasteHistoryViewSet
from backend_api.api.ViewSets.logging_changes_viewset import AdminLoggingChangesViewSet

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
    'logging':AdminLoggingChangesViewSet
}

router = DefaultRouter()

for route, viewset in ROUTE_VIEWSET_MAPPING.items():
    router.register(route, viewset)

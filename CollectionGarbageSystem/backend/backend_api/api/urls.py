from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, RoleUserViewSet, StationOfContainersStatusViewSet,
    StationOfContainersViewSet, CollectionSchedulesViewSet, NotificationTypesViewSet,
    NotificationsUserViewSet, StatusOfContainerViewSet, TypeOfContainerViewSet,
    ContainersViewSet, IoTFillingContainerViewSet, WasteHistoryViewSet
)

# Routers for each viewset

customer_router = DefaultRouter()
role_user_router = DefaultRouter()
station_of_containers_status_router = DefaultRouter()
station_of_containers_router = DefaultRouter()
collection_schedules_router = DefaultRouter()
notification_types_router = DefaultRouter()
notifications_user_router = DefaultRouter()
status_of_container_router = DefaultRouter()
type_of_container_router = DefaultRouter()
containers_router = DefaultRouter()
iot_filling_container_router = DefaultRouter()
waste_history_router = DefaultRouter()

# Registering viewsets with respective routes

customer_router.register(r'customers', CustomerViewSet)
role_user_router.register(r'roleUsers', RoleUserViewSet)
station_of_containers_status_router.register(r'stationOfContainersStatuses', StationOfContainersStatusViewSet)
station_of_containers_router.register(r'stationOfContainers', StationOfContainersViewSet)
collection_schedules_router.register(r'collectionSchedules', CollectionSchedulesViewSet)
notification_types_router.register(r'notificationTypes', NotificationTypesViewSet)
notifications_user_router.register(r'notificationsUsers', NotificationsUserViewSet)
status_of_container_router.register(r'statusOfContainers', StatusOfContainerViewSet)
type_of_container_router.register(r'typeOfContainers', TypeOfContainerViewSet)
containers_router.register(r'containers', ContainersViewSet)
iot_filling_container_router.register(r'iotFillingContainers', IoTFillingContainerViewSet)
waste_history_router.register(r'wasteHistories', WasteHistoryViewSet)

# You can then include these routers in your URL configuration

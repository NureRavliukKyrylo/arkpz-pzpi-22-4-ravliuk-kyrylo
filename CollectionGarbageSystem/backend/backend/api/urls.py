from rest_framework.routers import DefaultRouter
from backend_api.api.urls import (
    customer_router, role_user_router, station_of_containers_status_router,
    station_of_containers_router, collection_schedules_router, notification_types_router,
    notifications_user_router, status_of_container_router, type_of_container_router,
    containers_router, iot_filling_container_router, waste_history_router
)
from django.urls import path, include

router = DefaultRouter()

router.registry.extend(customer_router.registry)
router.registry.extend(role_user_router.registry)
router.registry.extend(station_of_containers_status_router.registry)
router.registry.extend(station_of_containers_router.registry)
router.registry.extend(collection_schedules_router.registry)
router.registry.extend(notification_types_router.registry)
router.registry.extend(notifications_user_router.registry)
router.registry.extend(status_of_container_router.registry)
router.registry.extend(type_of_container_router.registry)
router.registry.extend(containers_router.registry)
router.registry.extend(iot_filling_container_router.registry)
router.registry.extend(waste_history_router.registry)

urlpatterns = [
    path('', include(router.urls)),  
]

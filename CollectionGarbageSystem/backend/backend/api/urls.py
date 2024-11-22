from rest_framework.routers import DefaultRouter
from backend_api.api.urls import customer_router, role_user_router
from django.urls import path,include

router = DefaultRouter()

router.registry.extend(customer_router.registry)
router.registry.extend(role_user_router.registry)

urlpatterns = [
    path('', include(router.urls)),
]
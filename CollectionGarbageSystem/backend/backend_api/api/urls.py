from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, RoleUserViewSet

customer_router = DefaultRouter()
role_user_router = DefaultRouter()

customer_router.register(r'customers', CustomerViewSet)
role_user_router.register(r'roleUsers', RoleUserViewSet)
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from backend_api.views import MineTokenObtainPairView,RegisterCustomerView,LoginCustomerView, LogoutCustomerView, GetReportOfStationsView, GetReportOfContainersView,DownloadBackupView,RestoreBackupView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="CollectionGarbageSystem API",
        default_version='v1',
        description="Test For Task2",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourdomain.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.api.urls')),
    path('api/token/', MineTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register', RegisterCustomerView.as_view(), name='register_user'),
    path('api/login', LoginCustomerView.as_view(), name='login_user'),
    path('api/logout', LogoutCustomerView.as_view(), name='logout_user'),
    path('api/get_report',GetReportOfStationsView.as_view(),name = "report"),
    path('api/get_report_waste',GetReportOfContainersView.as_view(),name = "report"),
    path('api/back-up',DownloadBackupView.as_view(),name = "back_up"),
    path('api/restore-DB',RestoreBackupView.as_view(),name = "restore_db"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')

]
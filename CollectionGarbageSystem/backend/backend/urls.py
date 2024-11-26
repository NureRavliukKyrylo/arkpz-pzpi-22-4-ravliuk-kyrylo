from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from backend_api.views import MineTokenObtainPairView,registerCustomer,loginCustomer, logoutCustomer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.api.urls')),
    path('api/token/', MineTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register', registerCustomer, name='register_user'),
    path('api/login', loginCustomer, name='login_user'),
    path('api/logout', logoutCustomer, name='logout_user'),
]
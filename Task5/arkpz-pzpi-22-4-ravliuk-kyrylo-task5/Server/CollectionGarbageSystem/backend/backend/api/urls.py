from django.urls import path, include
from backend_api.api.urls import router

urlpatterns = [
    path('', include(router.urls)),
]
from rest_framework.viewsets import ModelViewSet
from backend_api.models import CustomUser,RoleUser
from .serializers import CustomerSerializer,RoleUserSerializer

class CustomerViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomerSerializer

class RoleUserViewSet(ModelViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleUserSerializer
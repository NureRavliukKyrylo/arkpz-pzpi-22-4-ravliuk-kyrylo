from rest_framework.serializers import ModelSerializer
from backend_api.models import CustomUser,RoleUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password','username', 'email', 'is_active', 'is_staff', 'role', 'date_joined']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_admin'] = user.is_superuser

        return token

class RoleUserSerializer(ModelSerializer):
    class Meta:
        model = RoleUser
        fields = ['name']
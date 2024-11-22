from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from backend_api.models import (
    CustomUser, RoleUser, StationOfContainers, StationOfContainersStatus, 
    CollectionSchedules, NotificationTypes, NotificationsUser, StatusOfContainer, 
    TypeOfContainer, Containers, IoTFillingContainer, WasteHistory
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password', 'username', 'email', 'is_active', 'is_staff', 'role', 'date_joined']

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

class StationOfContainersStatusSerializer(ModelSerializer):
    class Meta:
        model = StationOfContainersStatus
        fields = ['station_status_name']

class StationOfContainersSerializer(ModelSerializer):  
    class Meta:
        model = StationOfContainers
        fields = ['station_of_containers_name', 'latitude_location', 'longitude_location', 'status_station', 'last_reserved']

class CollectionSchedulesSerializer(ModelSerializer):
    class Meta:
        model = CollectionSchedules
        fields = ['station_of_containers_id', 'collection_date']

class NotificationTypesSerializer(ModelSerializer):
    class Meta:
        model = NotificationTypes
        fields = ['type_notification_name']

class NotificationsUserSerializer(ModelSerializer):
    class Meta:
        model = NotificationsUser
        fields = ['user_id', 'message', 'notification_type', 'timestamp_get_notification', 'station_id']

class StatusOfContainerSerializer(ModelSerializer):
    class Meta:
        model = StatusOfContainer
        fields = ['status_name']

class TypeOfContainerSerializer(ModelSerializer):
    class Meta:
        model = TypeOfContainer
        fields = ['type_name_container', 'volume_container']

class ContainersSerializer(ModelSerializer):
    class Meta:
        model = Containers
        fields = ['fill_level', 'status_container_id', 'last_updated', 'type_of_container_id', 'station_id']

class IoTFillingContainerSerializer(ModelSerializer):
    class Meta:
        model = IoTFillingContainer
        fields = ['container_id_filling', 'sensor_value', 'time_of_detect']

class WasteHistorySerializer(ModelSerializer):
    class Meta:
        model = WasteHistory
        fields = ['amount', 'station_id', 'recycling_date']
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from backend_api.models import (
    CustomUser, RoleUser, StationOfContainers, StationOfContainersStatus, 
    CollectionSchedules, NotificationTypes, NotificationsUser, StatusOfContainer, 
    TypeOfContainer, Containers, IoTFillingContainer, WasteHistory,AdminLoggingChanges
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.timezone import now
from django.contrib.auth.hashers import check_password
from .validators import (
    validate_only_letters, validate_latitude, validate_longitude, 
    validate_positive, validate_collection_date, validate_sensor_value,validate_amount_history
)

class CustomerSerializer(ModelSerializer):
    password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['password', 'username', 'email', 'is_active', 'is_staff', 'role', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password) 
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return super().update(instance, validated_data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token


class RoleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleUser
        fields = ['name']

    def validate_name(self, value):
        return validate_only_letters(value)


class StationOfContainersStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationOfContainersStatus
        fields = ['station_status_name']

    def validate_station_status_name(self, value):
        return validate_only_letters(value)

class StationOfContainersSerializer(serializers.ModelSerializer):  
    class Meta:
        model = StationOfContainers
        fields = ['station_of_containers_name', 'latitude_location', 'longitude_location', 'status_station', 'last_reserved']
    
    def validate_latitude_location(self, value):
        return validate_latitude(value)
    
    def validate_longitude_location(self, value):
        return validate_longitude(value)

class CollectionSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionSchedules
        fields = ['station_of_containers_id', 'collection_date']

    def validate_collection_date(self, value):
        return validate_collection_date(value)
    
    

class NotificationTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTypes
        fields = ['type_notification_name']

    def validate_name(self, value):
        return validate_only_letters(value)


class NotificationsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationsUser
        fields = ['user_id', 'message', 'notification_type', 'timestamp_get_notification', 'station_id']


class StatusOfContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusOfContainer
        fields = ['status_name']
    
    def validate_status_name(self, value):
        return validate_only_letters(value)


class TypeOfContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfContainer
        fields = ['type_name_container', 'volume_container']
    
    def validate_volume_container(self, value):
        return validate_positive(value)
    
    def validate_type_name_container(self, value):
        return validate_only_letters(value)
    

class ContainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Containers
        fields = ['fill_level', 'status_container_id', 'last_updated', 'type_of_container_id', 'station_id']


class IoTFillingContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoTFillingContainer
        fields = ['container_id_filling', 'sensor_value', 'time_of_detect']

    def validate_sensor_value(self, value):
        return validate_sensor_value(value)


class WasteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteHistory
        fields = ['amount', 'station_id', 'recycling_date']

    def validate_amount(self, value):
        return validate_amount_history(value)

    def validate_recycling_date(self, value):
        return validate_collection_date(value)

class RegisterCustomerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, data):
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username is already in use."})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class LoginCustomerSerializer(serializers.Serializer): 
    username = serializers.CharField(max_length=150) 
    password = serializers.CharField(write_only=True)

class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class PasswordUpdateSerializer(serializers.Serializer):
    last_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"}
    )

    def validate(self, data):
        user = self.context['user']
        if not check_password(data['last_password'], user.password):
            raise serializers.ValidationError({"last_password": "Incorrect password."})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    
class UpdateStationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationOfContainers
        fields = ['status_station']
        

class SensorValueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoTFillingContainer
        fields = ['sensor_value']

    def validate_sensor_value(self, value):
        return validate_sensor_value(value)
    
class CollectionScheduleUpdateDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionSchedules
        fields = ['collection_date']
    
    def validate_collection_date(self, value):
        return validate_collection_date(value)

class CustomerUpdateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_active', 'is_staff', 'role', 'date_joined']

class AdminLoggingChangesSerializer(ModelSerializer):
    class Meta:
        model = AdminLoggingChanges
        fields = ['user','table_name','action','timestamp','values']
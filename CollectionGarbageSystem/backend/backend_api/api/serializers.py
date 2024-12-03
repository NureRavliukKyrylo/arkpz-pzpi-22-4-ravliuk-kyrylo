from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from backend_api.models import (
    CustomUser, RoleUser, StationOfContainers, StationOfContainersStatus, 
    CollectionSchedules, NotificationTypes, NotificationsUser, StatusOfContainer, 
    TypeOfContainer, Containers, IoTFillingContainer, WasteHistory
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.timezone import now
from django.contrib.auth.hashers import check_password

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
        if not value.isalpha():
            raise serializers.ValidationError('The field may only contain letters.')
        return value


class StationOfContainersStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationOfContainersStatus
        fields = ['station_status_name']

    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('The field may only contain letters.')
        return value

class StationOfContainersSerializer(serializers.ModelSerializer):  
    class Meta:
        model = StationOfContainers
        fields = ['station_of_containers_name', 'latitude_location', 'longitude_location', 'status_station', 'last_reserved']
    
    def validate_latitude_location(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value
    
    def validate_longitude_location(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value


class CollectionSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionSchedules
        fields = ['station_of_containers_id', 'collection_date']

    def validate_collection_date(self, value):
        if value < now():
            raise serializers.ValidationError("The collection date cannot be in the past.")
        return value
    

class NotificationTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTypes
        fields = ['type_notification_name']

    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('The field may only contain letters.')
        return value


class NotificationsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationsUser
        fields = ['user_id', 'message', 'notification_type', 'timestamp_get_notification', 'station_id']


class StatusOfContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusOfContainer
        fields = ['status_name']
    
    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('The field may only contain letters.')
        return value


class TypeOfContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfContainer
        fields = ['type_name_container', 'volume_container']
    
    def validate_volume_container(self, value):
        if value <= 0:
            raise serializers.ValidationError("The container volume must be greater than 0.")
        return value
    
    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('The field may only contain letters.')
        return value


class ContainersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Containers
        fields = ['fill_level', 'status_container_id', 'last_updated', 'type_of_container_id', 'station_id']


class IoTFillingContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoTFillingContainer
        fields = ['container_id_filling', 'sensor_value', 'time_of_detect']

    def validate_sensor_value(self, value):
        if value > 100:
            raise serializers.ValidationError("The 'sensor_value' cannot exceed 100.")
        if value <= 0:
            raise serializers.ValidationError("The 'sensor_value' cannot be negative.")
        return value
    
    def validate_container_id_filling(self, value):
        if not Containers.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("A container with this ID does not exist.")
        return value


class WasteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteHistory
        fields = ['amount', 'station_id', 'recycling_date']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The amount of waste must be greater than 0.")
        return value

    def validate_recycling_date(self, value):
        if value < now().date():
            raise serializers.ValidationError("The recycling date cannot be in the past.")
        return value

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
        if value < 0: 
            raise serializers.ValidationError("Sensor value must be a positive number.")
        return value
    
class CollectionScheduleUpdateDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionSchedules
        fields = ['collection_date']
    
    def validate_collection_date(self, value):
        if value < now():
            raise serializers.ValidationError("The collection date cannot be in the past.")
        return value
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class RoleUser(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(RoleUser, on_delete=models.SET_NULL, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password'] 

    def __str__(self):
        return self.email


class StationOfContainersStatus(models.Model):
    station_status_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.station_status_name
    
class StationOfContainers(models.Model):
    station_of_containers_name = models.CharField(max_length=100)  
    latitude_location = models.FloatField()
    longitude_location = models.FloatField()
    status_station = models.ForeignKey(StationOfContainersStatus, on_delete=models.SET_NULL, null=True, blank=True)
    last_reserved = models.DateTimeField(unique=True)
    

    def __str__(self):
        return self.station_of_containers_name
    
class CollectionSchedules(models.Model):
    station_of_containers_id = models.ForeignKey(StationOfContainers, on_delete=models.SET_NULL, null=True, blank=True)
    collection_date = models.DateTimeField(unique=True)

    def __str__(self):
        return self.station_of_containers_id
    
class NotificationTypes(models.Model):
    type_notification_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type_notification_name

class NotificationsUser(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(max_length=150, unique=True)
    notification_type = models.ForeignKey(NotificationTypes, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp_get_notification = models.DateTimeField(unique=True)
    station_id = models.ForeignKey(StationOfContainers, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user_id

class StatusOfContainer(models.Model):
    status_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.status_name 

class TypeOfContainer(models.Model):
    type_name_container = models.CharField(max_length=150, unique=True)
    volume_container = models.FloatField()
    
    def __str__(self):
        return self.type_name_container

class Containers(models.Model):
    fill_level = models.FloatField()
    status_container_id = models.ForeignKey(StatusOfContainer, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField(unique=True)
    type_of_container_id = models.ForeignKey(TypeOfContainer, on_delete=models.SET_NULL, null=True, blank=True)
    station_id = models.ForeignKey(StationOfContainers, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
class IoTFillingContainer(models.Model):
    container_id_filling = models.ForeignKey(Containers, on_delete=models.SET_NULL, null=True, blank=True)
    sensor_value = models.FloatField()
    time_of_detect = models.DateTimeField(unique=True)

    def __str__(self):
        return f"Container with fill level: {self.fill_level:.2f}"
    
class WasteHistory(models.Model):
    amount = models.FloatField()
    station_id = models.ForeignKey(StationOfContainers, on_delete=models.SET_NULL, null=True, blank=True)
    recycling_date = models.DateTimeField(unique=True)

    def __str__(self):
        return str(self.recycling_date)  
    
    def save(self, *args, **kwargs):
        if self.station_id:  
            last_container_filling = IoTFillingContainer.objects.filter(
                container_id_filling__station_id=self.station_id
            ).last()  
            if last_container_filling:
                sensor_value = last_container_filling.sensor_value
                container = last_container_filling.container_id_filling
                container_volume = container.type_of_container_id.volume_container
                self.amount = sensor_value * container_volume
        super().save(*args, **kwargs) 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from backend_api.models import IoTFillingContainer, CustomUser, NotificationsUser, NotificationTypes, StatusOfContainer, StationOfContainers,WasteHistory, CollectionSchedules,StationOfContainersStatus
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(post_save, sender=IoTFillingContainer)
def check_container_fill_level(sender, instance, created, **kwargs):
    if created:
        container = instance.container_id_filling
        if container:
            if instance.sensor_value > 90:
                full_status, created = StatusOfContainer.objects.get_or_create(status_name="Full")
                container.status_container_id = full_status
                container.save()

                operators = CustomUser.objects.filter(role__name="Operator")
                if operators.exists():
                    for operator in operators:
                        NotificationsUser.objects.create(
                            user_id=operator,
                            message=f"Контейнер {container.id} на станції '{container.station_id.station_of_containers_name}' потребує обслуговування поза графіком.",
                            notification_type=NotificationTypes.objects.get_or_create(type_notification_name="Позапланове обслуговування")[0],
                            timestamp_get_notification=now(),
                            station_id=container.station_id
                        )
            elif instance.sensor_value < 90:
                active_status, created = StatusOfContainer.objects.get_or_create(status_name="Active")
                container.status_container_id = active_status
                container.save()

@receiver(pre_save, sender=StationOfContainers)
def update_last_reserved_on_status_change(sender, instance, **kwargs):
    if instance.pk: 
        previous_instance = StationOfContainers.objects.get(pk=instance.pk)
        
        if (previous_instance.status_station.station_status_name == "Reserving" and 
            instance.status_station.station_status_name == "Active"):
            instance.last_reserved = timezone.now() 

@receiver(post_save, sender=StationOfContainers)
def create_waste_history_on_status_change(sender, instance, **kwargs):
    if instance.pk: 
        previous_instance = StationOfContainers.objects.get(pk=instance.pk)
        
        if (previous_instance.status_station.station_status_name == "Reserving"):
            WasteHistory.objects.create(
                station_id=instance,
                recycling_date=instance.last_reserved,
            )

def get_reserving_status():
    return StationOfContainersStatus.objects.get_or_create(station_status_name="Reserving")[0]

@receiver(post_save, sender=CollectionSchedules)
def update_station_status_on_schedule(sender, instance, created, **kwargs):
    if not created:  
        return
    
    if instance.collection_date.date() == timezone.now().date():
        station = instance.station_of_containers_id
        station.status_station = get_reserving_status()
        station.save()
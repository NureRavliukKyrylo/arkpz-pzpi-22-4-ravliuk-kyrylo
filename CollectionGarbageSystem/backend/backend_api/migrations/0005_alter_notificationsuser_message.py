# Generated by Django 5.1.3 on 2024-11-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0004_rename_name_stationofcontainers_station_of_containers_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationsuser',
            name='message',
            field=models.CharField(max_length=150),
        ),
    ]

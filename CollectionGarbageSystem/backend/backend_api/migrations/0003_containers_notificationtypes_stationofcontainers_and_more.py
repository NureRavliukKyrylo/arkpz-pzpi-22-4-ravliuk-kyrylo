# Generated by Django 5.1.3 on 2024-11-22 17:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0002_customuser_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Containers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fill_level', models.FloatField()),
                ('last_updated', models.DateTimeField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_notification_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StationOfContainers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude_location', models.FloatField()),
                ('longitude_location', models.FloatField()),
                ('last_reserved', models.DateTimeField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StationOfContainersStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_status_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StatusOfContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name_container', models.CharField(max_length=150, unique=True)),
                ('volume_container', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IoTFillingContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_value', models.FloatField()),
                ('time_of_detect', models.DateTimeField(unique=True)),
                ('container_id_filling', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_api.containers')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationsUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=150, unique=True)),
                ('timestamp_get_notification', models.DateTimeField(unique=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('notification_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_api.notificationtypes')),
                ('station_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_api.stationofcontainers')),
            ],
        ),
        migrations.AddField(
            model_name='containers',
            name='station_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_api.stationofcontainers'),
        ),
        migrations.CreateModel(
            name='CollectionSchedules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_date', models.DateTimeField(unique=True)),
                ('station_of_containers_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_api.stationofcontainers')),
            ],
        ),
        migrations.AddField(
            model_name='stationofcontainers',
            name='status_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_api.stationofcontainersstatus'),
        ),
        migrations.AddField(
            model_name='containers',
            name='status_container_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_api.statusofcontainer'),
        ),
        migrations.AddField(
            model_name='containers',
            name='type_of_container_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_api.typeofcontainer'),
        ),
        migrations.CreateModel(
            name='WasteHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('recycling_date', models.DateTimeField(unique=True)),
                ('station_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_api.stationofcontainers')),
            ],
        ),
    ]
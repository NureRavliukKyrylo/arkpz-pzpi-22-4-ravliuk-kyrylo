# Generated by Django 5.1.3 on 2024-11-23 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0007_remove_containers_fill_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationofcontainers',
            name='last_reserved',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
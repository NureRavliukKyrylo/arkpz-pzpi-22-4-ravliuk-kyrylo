# Generated by Django 5.1.3 on 2024-11-23 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0005_alter_notificationsuser_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iotfillingcontainer',
            name='time_of_detect',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

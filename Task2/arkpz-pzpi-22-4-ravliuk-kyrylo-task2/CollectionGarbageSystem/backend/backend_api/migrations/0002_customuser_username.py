# Generated by Django 5.1.3 on 2024-11-22 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]

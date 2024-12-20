from rest_framework import serializers
from django.utils.timezone import now

def validate_date_range(data):
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not start_date or not end_date:
        raise ValueError("Missing 'start_date' or 'end_date'")

    return start_date, end_date

def validate_only_letters(value):
    if not value.isalpha():
        raise serializers.ValidationError("The field may only contain letters.")
    return value

def validate_latitude(value):
    if not (-90 <= value <= 90):
        raise serializers.ValidationError("Latitude must be between -90 and 90.")
    return value

def validate_longitude(value):
    if not (-180 <= value <= 180):
        raise serializers.ValidationError("Longitude must be between -180 and 180.")
    return value

def validate_positive(value):
    if value <= 0:
        raise serializers.ValidationError("This value must be greater than 0.")
    return value

def validate_collection_date(value):
    if value < now():
        raise serializers.ValidationError("The date cannot be in the past.")
    return value

def validate_sensor_value(value):
    if value > 100:
        raise serializers.ValidationError("The 'sensor_value' cannot exceed 100.")
    if value <= 0:
        raise serializers.ValidationError("The 'sensor_value' cannot be negative.")
    return value

def validate_amount_history(value):
    if value <= 0:
            raise serializers.ValidationError("The amount of waste must be greater than 0.")
    return value
from rest_framework import serializers
from core.models.service import Service, Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            'id',
            'day_name',
            'start_schedule',
            'end_schedule',
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id',
            'service_name',
            'proprietor',
            'service_category',
            'is_available',
            'service_schedule',
            'price',
            'commission',
            'discount_price',
            'short_description',
            'service_image',
            'galley_image',
            'galley_image2',
            'galley_image3',
            'created_at',
            'updated_at',
        ]

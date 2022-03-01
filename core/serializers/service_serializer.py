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

    def validate_service_name(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError("Item name should be more than 5 characters")
        return value

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['service_schedule'] = ScheduleSerializer(instance.service_schedule).data
        return response

from rest_framework import serializers
from task.models.service import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'manager', 'services', 'is_active',
            'created_at', 'updated_at'
        ]

from rest_framework import serializers

from core.models.location import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'id', 'name', 'parent', 'is_active', 'location_image', 'location_type',
            'get_city_queryset', 'get_postcode_queryset', 'get_thana_queryset',
            'children_count', 'created_at', 'updated_at'
        )

    def validate_name(self, value):
        if len(value) <= 2:
            raise serializers.ValidationError("Name should be more than 2 characters")
        return value

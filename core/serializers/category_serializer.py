from rest_framework import serializers
from core.models.category import Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id', 'name'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'parent', 'is_active', 'image',
            'children_count', 'created_at', 'updated_at'
        )

    def validate_name(self, value):
        if len(value) <= 2:
            raise serializers.ValidationError("Name should be more than 2 characters")
        return value

from rest_framework import serializers
from core.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'parent', 'is_active', 'image',
            'children_count', 'created_at', 'updated_at'
        )

from rest_framework import serializers

from task.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'order', 'banner', 'created_at', 'updated_at')

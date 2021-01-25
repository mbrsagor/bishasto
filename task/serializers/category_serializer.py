from rest_framework import serializers

from task.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'order', 'isActive', 'created_at', 'updated_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['parent'] = CategorySerializer(instance.parent).data
        return response

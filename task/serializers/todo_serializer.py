from rest_framework import serializers
from task.models.todo import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'created_by',
            'is_active',
            'created_at',
            'updated_at'
        ]

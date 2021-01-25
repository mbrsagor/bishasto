from rest_framework import serializers

from task.models.task import Task, TaskManager
from task.serializers.user_seralizer import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['created_by'] = UserSerializer(instance.created_by).data
        return response


class TaskManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskManager
        fields = (
            'id', 'tasks', 'task_status', 'start_time', 'end_time', 'is_active',
            'calculation', 'created_at', 'updated_at'
        )

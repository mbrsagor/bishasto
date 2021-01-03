from rest_framework import serializers

from task.models.task import Task, TaskManager


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by']


class TaskManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskManager
        fields = (
            'id', 'tasks', 'manage_by', 'task_status', 'start_time', 'end_time', 'is_active',
            'calculation', 'created_at', 'updated_at'
        )
        read_only_fields = ['manage_by']

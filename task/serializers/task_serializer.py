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
        fields = '__all__'
        read_only_fields = ['manage_by']

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from task.models.task import Task, TaskManager
from task.serializers.task_serializer import TaskSerializer, TaskManagerSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.request.user.taskCreator.all()


class TaskManagerViewSet(ModelViewSet):
    queryset = TaskManager.objects.all()
    serializer_class = TaskManagerSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.request.user.taskManageBy.all()

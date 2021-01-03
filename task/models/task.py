from django.db import models
from django.contrib.auth.models import User

from task.models.base import BaseEntity
from task.models.category import Category
from task.utils import TaskStatus


class Task(BaseEntity):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.BooleanField(default=True)
    task_picture = models.ImageField(upload_to='task', null=True, blank=True)
    task_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='addTask')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taskCreator')

    def __str__(self):
        return self.name[:40]


class TaskManager(BaseEntity):
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, related_name='task')
    manage_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taskManageBy')
    task_status = models.IntegerField(choices=TaskStatus.get_choices(), default=TaskStatus.RUNNING.value)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tasks.name if self.tasks and self.tasks.name else ""

    # Task calculation
    def calculation(self):
        result = self.end_time - self.start_time
        return result

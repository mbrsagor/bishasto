from django.db import models
from django.contrib.auth.models import User

from task.models.base import BaseEntity
from task.models.category import Category


class Task(BaseEntity):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.BooleanField(default=True)
    task_picture = models.ImageField(upload_to='task')
    task_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='addTask')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taskCreator')

    def __str__(self):
        return self.name[:40]


class TaskManager(BaseEntity):
    title = models.CharField(max_length=50)
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, related_name='task')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

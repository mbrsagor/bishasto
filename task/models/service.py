from django.db import models
from django.db.models import JSONField

from task.models.base import BaseEntity
from task.models.task import TaskManager


class Service(BaseEntity):
    name = models.CharField(max_length=90)
    manager = models.ForeignKey(TaskManager, on_delete=models.CASCADE, related_name='service_manager', blank=True)
    services = JSONField(default=None, null=True, blank=True)
    is_active = models.BooleanField(blank=True)

    def __str__(self):
        return self.name[:40]

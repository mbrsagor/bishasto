from django.db import models
from task.models.base import BaseEntity


class Todo(BaseEntity):
    title = models.CharField(max_length=70)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title[:40]

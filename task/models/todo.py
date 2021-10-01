from django.db import models
from task.models.base import BaseEntity
from account.models import User


class Todo(BaseEntity):
    title = models.CharField(max_length=70)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='todoUser')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title[:40]

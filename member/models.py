from django.db import models
from django.contrib.auth.models import User

from task.models.base import BaseEntity
from task.utils import Gender


class Profile(BaseEntity):
    user = models.OneToOneField(User, related_name='userProfile')
    phone_number = models.CharField(max_length=14)
    address = models.TextField(default='')
    age = models.IntegerField(default=0)
    # gender = models.IntegerChoices(Gender.select_gender())

    def __str__(self):
        return self.user.username

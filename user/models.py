from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager
from utils.enum import GENDER, ROLE


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=14, unique=True)
    role = models.IntegerField(choices=ROLE.get_choices(), default=ROLE.CUSTOMER.value)
    gender = models.IntegerField(choices=GENDER.select_gender(), default=GENDER.MALE.value)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(default=datetime.now)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']
    objects = UserManager()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return str(self.email)

    @property
    def current_age(self):
        today = date.today()
        return (today - self.date_of_birth).days

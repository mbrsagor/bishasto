from datetime import date, datetime
from django.db import models

from core.models.base import Timestamp
from core.models.location import Location
from user.models import User


class Shop(Timestamp):
    shop_name = models.CharField(max_length=120, unique=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_owner')
    shop_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')
    is_available = models.BooleanField(default=True)
    tread_license = models.TextField()
    address = models.TextField()
    shop_created_date = models.DateField(default=datetime.now)
    documents = models.FileField(upload_to='documents/%y/%m', blank=True, null=True)
    shop_image = models.ImageField(upload_to='shop/%y/%m', blank=True, null=True)

    def __str__(self):
        return self.shop_name[:50]

    def current_shop_age(self):
        today = date.today()
        return (today - self.shop_created_date).days

    def location_humanity(self):
        location = self.shop_location.name
        return location

    def owner_humanity(self):
        owner = self.owner.username
        return owner

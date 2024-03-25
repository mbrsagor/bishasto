from django.db import models
from core.models.base import Timestamp
from core.models.category import Category
from core.models.shop import Shop


class Schedule(Timestamp):
    day_name = models.CharField(max_length=30)
    start_schedule = models.TimeField()
    end_schedule = models.TimeField()

    def __str__(self):
        return self.day_name


class Service(Timestamp):
    service_name = models.CharField(max_length=120)
    proprietor = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop')
    service_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    is_available = models.BooleanField(default=True)
    service_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='schedules')
    price = models.DecimalField(max_digits=20, decimal_places=10)
    commission = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    discount_price = models.DecimalField(max_digits=20, decimal_places=10)
    short_description = models.TextField(default='')
    service_image = models.ImageField(upload_to='service/%y/%m', blank=True, null=True)
    galley_image = models.ImageField(upload_to='service/%y/%m', blank=True, null=True)
    galley_image2 = models.ImageField(upload_to='service/%y/%m', blank=True, null=True)
    galley_image3 = models.ImageField(upload_to='service/%y/%m', blank=True, null=True)

    def __str__(self):
        return self.service_name[:50]

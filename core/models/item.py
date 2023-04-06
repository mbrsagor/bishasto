from django.db import models

from core.models.base import BaseEntity
from core.models.category import Category, Tag
from core.models.shop import Shop
from utils.enum import TYPES


class Color(BaseEntity):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=8, unique=True, blank=True, default='#f00')

    def __str__(self):
        return self.name



class Item(BaseEntity):
    item_name = models.CharField(max_length=120)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    proprietor = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='item_shop')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='item_category')
    tags = models.ManyToManyField(Tag, related_name='item_tag')
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    commission = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    discount_price = models.DecimalField(max_digits=20, decimal_places=10)
    short_description = models.TextField(default='')
    model = models.TextField(max_length=60, blank=True, null=True)
    item_type = models.IntegerField(choices=TYPES.select_types(), default=TYPES.KG.value)
    item_image = models.ImageField(upload_to='item/%y/%m', blank=True, null=True)
    galley_image = models.ImageField(upload_to='gallery/%y/%m', blank=True, null=True)
    galley_image2 = models.ImageField(upload_to='gallery/%y/%m', blank=True, null=True)
    galley_image3 = models.ImageField(upload_to='gallery/%y/%m', blank=True, null=True)

    def __str__(self):
        return self.item_name[:50]

    def commission_price(self):
        return self.discount_price - self.discount_price

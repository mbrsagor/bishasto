from django.db import models
from core.models.base import BaseEntity
from core.models.item import Item
from django.conf import settings
from utils.enum import PROGRESS, PAYMENT


class Order(BaseEntity):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='customer')
    item_name = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
    reference = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    address = models.TextField(default='')
    transition_id = models.CharField(max_length=90, blank=True, null=True, unique=True)
    phone_number = models.TextField(max_length=60, blank=True, null=True)
    payment_type = models.IntegerField(choices=PAYMENT.payment_choices(), default=PAYMENT.CASH_ON_DELIVERY.value)
    status = models.IntegerField(choices=PROGRESS.order_status(), default=PROGRESS.PENDING.value)

    def __str__(self):
        return self.item_name.item_name

    @property
    def total_price(self):
        return self.item_name.price * self.quantity

    @property
    def owner_price(self):
        return self.total_price - self.item_name.commission

    @property
    def commission_price(self):
        return self.item_name.commission

    @property
    def shop_name(self):
        return self.item_name.proprietor.shop_name

import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.core.mail import send_mail
from django.dispatch import receiver

from core.models.base import BaseEntity
from core.models.item import Item
from django.conf import settings
from utils.enum import PROGRESS, PAYMENT


class Order(BaseEntity):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='customer')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=1)
    is_complete = models.BooleanField(default=True)

    def __str__(self):
        return self.item.item_name

    @property
    def total_price(self):
        return self.item.price * self.quantity

    @property
    def owner_price(self):
        return self.total_price - self.item.commission

    @property
    def commission_price(self):
        return self.item.commission

    @property
    def shop_name(self):
        return self.item.proprietor.shop_name


class OrderItem(BaseEntity):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                 related_name='OrderItemCustomer')
    orders = models.ManyToManyField(Order, related_name='orderItems')
    delivery_charge = models.IntegerField(default=0)
    address = models.TextField()
    transition_id = models.CharField(max_length=90, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=14)
    reference = models.CharField(max_length=200, blank=True, null=True)
    order_ide = models.CharField(max_length=25, blank=True, null=True, unique=True)
    payment_type = models.IntegerField(choices=PAYMENT.payment_choices(), default=PAYMENT.CASH_ON_DELIVERY.value)
    status = models.IntegerField(choices=PROGRESS.order_status(), default=PROGRESS.PENDING.value)

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        system_code = self.order_ide
        if not system_code:
            system_code = uuid.uuid4().hex[:6].upper()
        while OrderItem.objects.filter(order_ide=system_code).exclude(pk=self.pk).exists():
            system_code = uuid.uuid4().hex[:6].upper()
        self.order_ide = system_code
        super(OrderItem, self).save(*args, **kwargs)

    @receiver(pre_save, sender=Order)
    def active(sender, instance, **kwargs):
        if instance.is_active and OrderItem.objects.filter(pk=instance.pk).exists():
            subject = 'Add New Order'
            message = f'The order has been successfully completed. Order ID: {instance.pk}'
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, [instance.email], fail_silently=False)

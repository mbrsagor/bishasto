from django.db import models
from django.db.models.signals import post_save
from core.models.base import Timestamp


class SiteSetting(Timestamp):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self): return self.name


class Preference(Timestamp):
    site = models.OneToOneField(SiteSetting, on_delete=models.CASCADE, related_name='site_settings')
    site_name = models.CharField(max_length=120, default='your website name', blank=True, null=True)
    copyright = models.CharField(max_length=120, default='©Copyright 2022 | bishasto All Rights Reserved', blank=True,
                                 null=True)
    logo = models.ImageField(upload_to='preference', blank=True, null=True)
    footer_logo = models.ImageField(upload_to='footer_logo', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicon', blank=True, null=True)

    def __str__(self):
        return self.site.name

    @property
    def get_logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        else:
            return "/static/images/avatar.svg"


def create_preference(sender, instance, created, **kwargs):
    if created:
        preference, created = Preference.objects.get_or_create(site=instance)
        return preference


post_save.connect(create_preference, sender=SiteSetting)

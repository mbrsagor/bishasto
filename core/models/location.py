from django.db import models
from core.models.base import BaseEntity
from utils.enum import LOCATIONCHOICES


class Location(BaseEntity):
    name = models.CharField(max_length=120, unique=True)
    location_type = models.IntegerField(choices=LOCATIONCHOICES.location_type_choices(),
                                        default=LOCATIONCHOICES.DIVISION.value)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='mainArea', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    location_image = models.ImageField(upload_to='location/%y/%m', blank=True, null=True)

    def __str__(self):
        return self.name[:50]

    def children_count(self):
        return Location.objects.filter(parent=self).count()

    @staticmethod
    def get_city_queryset():
        return Location.objects.filter(location_type=1)

    @staticmethod
    def get_area_queryset():
        return Location.objects.filter(location_type=2)

    @staticmethod
    def get_thana_queryset():
        return Location.objects.filter(location_type=3)

    @staticmethod
    def get_postcode_queryset():
        return Location.objects.filter(location_type=4)

    @staticmethod
    def get_division_queryset():
        return Location.objects.filter(location_type=5)

    def to_string(self):
        locations = []
        starts = self
        while starts:
            locations.append(starts.name)
            try:
                starts = starts.parent
            except Exception as e:
                starts = None
        return ', '.join(locations)

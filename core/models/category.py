from django.db import models
from core.models.base import BaseEntity


class Category(BaseEntity):
    name = models.CharField(max_length=90)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='category', blank=True, null=True,
                               default=None)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='category/%y/%m', blank=True, null=True)

    def __str__(self):
        return self.name[:30]

    def get_children(self):
        return Category.objects.filter(parent=self)

    def children_count(self):
        return Category.objects.filter(parent=self).count()


class Tag(BaseEntity):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

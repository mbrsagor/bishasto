from django.db import models
from task.models.base import BaseEntity


class Category(BaseEntity):
    name = models.CharField(max_length=70)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='category')
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name[:40]

    def clean(self):
        pass

    def get_children(self):
        return Category.objects.filter(parent=self)

    def children_count(self):
        return Category.objects.filter(parent=self).count()

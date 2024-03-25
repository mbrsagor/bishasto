from django.db import models
from core.models.base import Timestamp
from cloudinary.models import CloudinaryField


class Category(Timestamp):
    name = models.CharField(max_length=90)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='category', blank=True, null=True,
                               default=None)
    is_active = models.BooleanField(default=True)
    image = CloudinaryField('category',  null=True, blank=True)

    def __str__(self):
        return self.name[:30]

    def get_children(self):
        return Category.objects.filter(parent=self)

    def children_count(self):
        return Category.objects.filter(parent=self).count()


class Tag(Timestamp):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

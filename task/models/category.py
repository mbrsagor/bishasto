from django.db import models
from django.contrib.auth.models import User
from task.models.base import BaseEntity


class Category(BaseEntity):
    name = models.CharField(max_length=70)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='category')
    order = models.IntegerField(default=999)
    banner = models.ImageField(upload_to='category', blank=True, null=True)

    def __str__(self):
        return self.name[:40]

    def clean(self):
        pass

    def get_children(self):
        return Category.objects.filter(parent=self)

    def children_count(self):
        return Category.objects.filter(parent=self).count()


class Post(BaseEntity):
    title = models.CharField(max_length=120)
    post_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='post_category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title[:50]

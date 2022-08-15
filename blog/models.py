from django.db import models

from core.models.base import BaseEntity
from user.models import User


class Post(BaseEntity):
    content = models.CharField(max_length=240)
    voters = models.ManyToManyField(User, related_name="votes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    content = models.CharField(max_length=240)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return self.content + ' of ' + self.post.content

    class Meta:
        verbose_name_plural = 'Comments'

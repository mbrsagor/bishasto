from rest_framework import serializers

from task.models.category import Category, Post
from task.serializers.user_seralizer import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'order', 'banner', 'created_at', 'updated_at')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['post_category'] = CategorySerializer(instance.post_category).data
        response['author'] = UserSerializer(instance.author).data
        return response

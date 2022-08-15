from rest_framework import generics

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


class PostCreateListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()



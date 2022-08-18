from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from utils.response import prepare_success_response, prepare_error_response


class PostCreateListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=self.request.user)
                return Response(prepare_success_response(serializer.data), status=status.HTTP_201_CREATED)
            return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(prepare_error_response(str(ex)), status=status.HTTP_400_BAD_REQUEST)


class CommentAddListAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=self.request.user)
                return Response(prepare_success_response(serializer.data), status=status.HTTP_201_CREATED)
            return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response(prepare_error_response(str(ex)), status=status.HTTP_400_BAD_REQUEST)

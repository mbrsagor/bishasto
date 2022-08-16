from django.urls import path
from .views import PostCreateListView, CommentAddListAPIView

urlpatterns = [
    path('post/', PostCreateListView.as_view()),
    path('comments/', CommentAddListAPIView.as_view()),
]

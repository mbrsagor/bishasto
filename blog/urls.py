from django.urls import path
from .views import PostCreateListView

urlpatterns = [
    path('post/', PostCreateListView.as_view())
]

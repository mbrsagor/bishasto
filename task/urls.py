from rest_framework.routers import DefaultRouter
from django.urls.conf import path

from task.views.category_view import CategoryViewSet, PostViewSet
from task.views.task_views import TaskViewSet, TaskManagerViewSet
from task.views.user_view import UserAPIView

router = DefaultRouter()

router.register('category', CategoryViewSet)
router.register('post', PostViewSet)
router.register('task', TaskViewSet)
router.register('task-manager', TaskManagerViewSet)

urlpatterns = [
    path('user', UserAPIView.as_view())
] + router.urls


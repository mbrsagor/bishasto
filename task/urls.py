from rest_framework.routers import DefaultRouter
from django.urls.conf import path

from task.views.category_view import CategoryViewSet
from task.views.task_views import TaskViewSet, TaskManagerViewSet
from task.views.user_view import UserAPIView, CustomJWTView

router = DefaultRouter()

router.register('category', CategoryViewSet)
router.register('task', TaskViewSet)
router.register('task-manager', TaskManagerViewSet)

urlpatterns = [
    path('user', UserAPIView.as_view()),
    path('login/', CustomJWTView.as_view()),
] + router.urls


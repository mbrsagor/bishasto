from rest_framework.routers import DefaultRouter
from django.urls.conf import path

from task.views.category_view import CategoryViewSet
from task.views.task_views import TaskViewSet, TaskManagerViewSet
from task.views.user_view import UserAPIView, CustomJWTView
from task.views.service_views import ServiceAPIView

router = DefaultRouter()

router.register('category', CategoryViewSet)
router.register('task', TaskViewSet)
router.register('task-manager', TaskManagerViewSet)

urlpatterns = [
    # User API endpoint
    path('user', UserAPIView.as_view()),
    path('login/', CustomJWTView.as_view()),
    # Service API endpoint
    path('services/', ServiceAPIView.as_view()),
    path('services/<int:pk>/', ServiceAPIView.as_view()),
    path('services/delete/<int:pk>/', ServiceAPIView.as_view()),
] + router.urls


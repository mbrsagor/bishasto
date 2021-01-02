from rest_framework.routers import DefaultRouter

from task.views.category_view import CategoryViewSet
from task.views.task_views import TaskViewSet, TaskManagerViewSet

router = DefaultRouter()

router.register('category', CategoryViewSet)
router.register('task', TaskViewSet)
router.register('task-manager', TaskManagerViewSet)

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from task.views.category_view import CategoryViewSet

router = DefaultRouter()

router.register('category', CategoryViewSet)

urlpatterns = router.urls

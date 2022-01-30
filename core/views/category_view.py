from rest_framework import permissions, viewsets

from core.serializers.category_serializer import CategorySerializer
from core.models.category import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

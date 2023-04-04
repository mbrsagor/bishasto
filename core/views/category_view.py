from rest_framework import permissions, viewsets

from core.serializers.category_serializer import CategorySerializer
from core.models.category import Category


class CategoryViewSet(viewsets.ModelViewSet):
    """"
    Name: Category API View
    URL:/api/v1/category/
    Method: GET, POST, PUT, DELETE
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

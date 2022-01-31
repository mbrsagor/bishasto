from rest_framework import viewsets, permissions

from core.models.service import Service, Schedule
from core.serializers.service_serializer import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Service.objects.filter(proprietor=self.request.user.shop_owner)
        else:
            return Service.objects.all()

    def perform_create(self, serializer):
        serializer.save(proprietor=self.request.user.shop_owner)

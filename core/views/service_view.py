from rest_framework import viewsets, permissions

from core.models.service import Service, Schedule
from core.serializers.service_serializer import ServiceSerializer, ScheduleSerializer
from utils.enum import ROLE


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_superuser:
            try:
                return Service.objects.filter(proprietor=self.request.user.shop_owner)
            except Exception as e:
                return str(e)
        else:
            return Service.objects.all()

    def perform_create(self, serializer):
        serializer.save(proprietor=self.request.user.shop_owner)

    # def create(self, request, *args, **kwargs):
    #     if self.request.user.role in (ROLE.ADMIN, ROLE.MANAGER, ROLE.SHOPKEEPER):
    #         pass


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAdminUser]

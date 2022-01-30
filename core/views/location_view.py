from rest_framework import viewsets, permissions
from core.models.location import Location
from core.serializers.location_serializer import LocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

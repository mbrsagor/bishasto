from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from task.serializers.user_seralizer import UserSerializer


class UserAPIView(APIView):
    # permission_classes = [permissions.AllowAny]

    def get(self, request):
        queryset = User.objects.get(user=self.request.user)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

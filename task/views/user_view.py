from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from task.serializers.user_seralizer import UserSerializer


class UserAPIView(APIView):

    def get(self, request):
        try:
            queryset = User.objects.get(id=self.request.user.id)
            serializer = UserSerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "message": "Sorry! you are not a authentication user.",
                "status": status.HTTP_404_NOT_FOUND
            })

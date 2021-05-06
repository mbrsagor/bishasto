from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from task.serializers.user_seralizer import UserSerializer, TokenObtainTokenSerializer


class UserAPIView(APIView):

    def get(self, request):
        try:
            queryset = User.objects.get(id=self.request.user.id)
            serializer = UserSerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({
                "message": "Sorry! Authentication credentials were not provided.",
                "status": status.HTTP_404_NOT_FOUND
            })


class CustomJWTView(TokenObtainPairView):
    serializer_class = TokenObtainTokenSerializer

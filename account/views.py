from rest_framework import views, status, permissions
from rest_framework.response import Response

from .models import User
from .serializer import UserSerializer


class UserAPIView(views.APIView):
  permission_classes = [permissions.AllowAny, ]
  
  def post(self, request):
    try:
      pass
    except Exception as e:
        print(e)
        return Response(
            {"error": f"Something went to wrong registering and account. Exception: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
  

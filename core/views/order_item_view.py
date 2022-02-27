from django.core.mail import send_mail
from django.conf import settings
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response

from core.models.order import OrderItem
from core.serializers.order_seralizer import OrderItemSerializer
from utils.response import prepare_success_response, prepare_create_success_response, prepare_error_response


class OrderItemCreateListAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            order_item = OrderItem.objects.filter(status=0, customer=self.request.user)
            serializer = OrderItemSerializer(order_item, many=True)
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
    #
    # def post(self, request):
    #     pass

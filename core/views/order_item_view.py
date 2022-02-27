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
            items = serializer.data
            _price = []
            _quantity = []
            _total_price = 0
            for item in items:
                for i in item['orders']:
                    item_quantity = i['quantity']
                    _quantity.append(item_quantity)
                    item_price = i['item_name']['price']
                    _price.append(item_price)

            # price_str_to_float_convert = sum(float(sub) for sub in _price)
            price_convert_to_integer = [float(i) for i in _price]
            print(price_convert_to_integer)
            print(sum(_quantity))
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

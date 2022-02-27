from django.core.mail import send_mail
from django.conf import settings
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response

from core.models.order import OrderItem
from core.serializers.order_seralizer import OrderItemSerializer
from utils.response import prepare_success_response, prepare_create_success_response, prepare_error_response


class OrderItemCreateAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            order_item = OrderItem.objects.filter(status=0, customer=self.request.user)
            serializer = OrderItemSerializer(order_item, many=True)

            items = serializer.data
            _price = []
            _quantity = []
            for item in items:
                for order in item['orders']:
                    item_quantity = order['quantity']
                    _quantity.append(item_quantity)
                    item_price = order['item_name']['price']
                    _price.append(item_price)
            # price_str_to_float_convert = sum(float(sub) for sub in _price)

            # Calculations price
            price_convert_to_integer = [float(i) for i in _price]
            _delivery_charge = item['delivery_charge']
            sub_total = [num1 * num2 for num1, num2 in zip(price_convert_to_integer, _quantity)]
            calculate_sub_total = sum(sub_total)
            calculate_total_price = calculate_sub_total + _delivery_charge
            response = {
                'data': serializer.data,
                'sub_total': calculate_sub_total,
                'total': calculate_total_price
            }
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from django_filters import rest_framework as filters

from utils.enum_utils import ROLE
from core.models.order import OrderItem
from utils.filters import OrderItemFilter
from core.serializers import order_seralizer
from utils.pagination import StandardResultsSetPagination
from utils.message import PERMISSION, NOTFOUND, NO_CONTENT, DELETED
from utils.response import prepare_success_response, prepare_create_success_response, prepare_error_response


class OrderItemCalculation(object):
    """
    Order Item calculation model
    """
    def __init__(self, serializer):
        self.serializer = serializer

    def calculation_price(self):
        items = self.serializer
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
            'sub_total': calculate_sub_total,
            'delivery_charge': _delivery_charge,
            'total': calculate_total_price
        }
        return response


class OrderItemCreateAPIView(views.APIView):
    """
    Name: Order list view
    URL: /api/v1/order-item/
    Method: GET
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            order_item = OrderItem.objects.filter(status=0, customer=self.request.user)
            serializer = order_seralizer.OrderItemSerializer(order_item, many=True)
            calculation_order = OrderItemCalculation(serializer.data)
            response = {
                'data': calculation_order.serializer,
                'price_model': calculation_order.calculation_price()
            }
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)


class CreateOrderItemView(views.APIView):
    """
    Name: Order create list view
    URL: /api/v1/create-order/
    Method: POST
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = order_seralizer.CreateOrderItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
            return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)


class OrderItemDetailUpdateDeleteView(views.APIView):
    """
    Name: Order update, details and delete API
    URL: /api/v1/orderitem/<pk>/
    :param
    PK
    Method: GET, PUT, DELETE
    """
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, pk):
        try:
            return OrderItem.objects.get(id=pk)
        except OrderItem.DoesNotExist:
            return None

    def get(self, request, pk):
        order_item = self.get_object(pk)
        serializer = order_seralizer.OrderItemSerializer(order_item)
        if serializer is not None:
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        return Response(prepare_error_response(NO_CONTENT), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if request.user.role == ROLE.ADMIN or request.user.role == ROLE.MANAGER or request.user.role == ROLE.SHOPKEEPER:
            try:
                order_item = self.get_object(pk)
                serializer = order_seralizer.OrderItemSerializer(order_item, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
                return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(prepare_error_response(PERMISSION), status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        if request.user.role == ROLE.ADMIN or request.user.role == ROLE.MANAGER or request.user.role == ROLE.SHOPKEEPER:
            order_item = self.get_object(pk)
            if order_item is not None:
                order_item.delete()
                return Response(prepare_success_response(DELETED), status=status.HTTP_200_OK)
            return Response(prepare_error_response(NOTFOUND), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(prepare_error_response(PERMISSION), status=status.HTTP_401_UNAUTHORIZED)


class OrderItemFilterListView(generics.ListAPIView):
    """
    Name Order item filter
    URL: /api/v1/orderitem-filter
    Method: Get
    @params:
    phone_number, transition_id, status
    """
    queryset = OrderItem.objects.all()
    serializer_class = order_seralizer.OrderItemSerializer
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderItemFilter

    def list(self, request, *args, **kwargs):
        order_item = OrderItem.objects.all()
        serializer = order_seralizer.OrderItemSerializer(order_item, many=True)
        calculation_order = OrderItemCalculation(serializer.data)
        response = {
            'data': calculation_order.serializer,
            'price_model': calculation_order.calculation_price()
        }
        return Response(prepare_success_response(response), status=status.HTTP_200_OK)

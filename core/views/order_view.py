from rest_framework import views, generics, status, permissions
from django_filters import rest_framework as filters
from rest_framework.response import Response

from core.models.order import Order
from utils.filters import OrderFilter
from utils import response as custom_response
from utils import enum_utils, fcm, message, pagination
from core.serializers.order_seralizer import OrderSerializer


class OrderCreateListAPIView(views.APIView):
    """
    Name: Order create and listview API.
    URL: /api/v1/orders
    Method: GET, POST
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        if request.user.is_superuser:
            order = Order.objects.all()
        else:
            order = Order.objects.filter(user=self.request.user)
        if order is not None:
            serializer = OrderSerializer(order, many=True)
            return Response(custom_response.prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(custom_response.prepare_error_response(message.NO_CONTENT), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                # FCM notification for android and IOS user
                fcm.send_notification('device_token',  'FCM title here', 'FCM message here.')
                return Response(custom_response.prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
            return Response(custom_response.prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(custom_response.prepare_error_response(str(e)), status=status.HTTP_404_NOT_FOUND)


class OrderStatusUpdateDetailsAPIView(views.APIView):
    """
    Name: Order update API
    Desc: admin can confirm, cancel or progress update the order
    Method: PUT
    URL: /api/v1/order-update/
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        if serializer is not None:
            return Response(custom_response.prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        return Response(custom_response.prepare_error_response(message.NO_CONTENT), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            if request.user.role == enum_utils.ROLE.ADMIN or request.user.role == enum_utils.ROLE.MANAGER or request.user.role == enum_utils.ROLE.SHOPKEEPER:
                order = self.get_object(pk)
                if order is not None:
                    serializer = OrderSerializer(order, data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(user=self.request.user)
                        return Response(custom_response.prepare_create_success_response(serializer.data),
                                        status=status.HTTP_201_CREATED)
                    return Response(custom_response.prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(custom_response.prepare_error_response(message.NOTFOUND),
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(custom_response.prepare_error_response(message.PERMISSION), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(custom_response.prepare_error_response(str(e)), status=status.HTTP_404_NOT_FOUND)


class OrderFilterListView(generics.ListAPIView):
    """
    Name: Order filter API
    URL: /api/v1/order-filter/
    Method: GET
    params: name, OrderID
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

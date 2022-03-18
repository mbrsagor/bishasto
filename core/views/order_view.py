from rest_framework import views, generics, status, permissions
from django_filters import rest_framework as filters
from rest_framework.response import Response

from core.models.order import Order
from core.serializers.order_seralizer import OrderSerializer
from utils.response import prepare_success_response, prepare_error_response, prepare_create_success_response
from utils.pagination import StandardResultsSetPagination
from utils.filters import OrderFilter
from utils.enum import ROLE


class OrderCreateListAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        if request.user.is_superuser:
            order = Order.objects.all()
        else:
            order = Order.objects.filter(user=self.request.user)
        if order is not None:
            serializer = OrderSerializer(order, many=True)
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(prepare_error_response("Content Not found"), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
        return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class OrderStatusUpdateDetailsAPIView(views.APIView):
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
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        return Response(prepare_error_response("Content Not found"), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if request.user.role == ROLE.ADMIN or request.user.role == ROLE.MANAGER or request.user.role == ROLE.SHOPKEEPER:
            order = self.get_object(pk)
            if order is not None:
                serializer = OrderSerializer(order, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(user=self.request.user)
                    return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
                return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(prepare_error_response("No data found for this ID"), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(prepare_error_response('You have no permission'), status=status.HTTP_400_BAD_REQUEST)


class OrderFilterListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

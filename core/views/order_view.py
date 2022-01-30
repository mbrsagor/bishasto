from rest_framework import views, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from core.models.order import Order
from core.serializers.order_seralizer import OrderSerializer, OrderStatusUpdateSerializer
from utils.response import prepare_success_response, prepare_error_response, prepare_create_success_response


class OrderCreateListAPIView(views.APIView):

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
        order = self.get_object(pk)
        if order is not None:
            serializer = OrderStatusUpdateSerializer(order, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=self.request.user)
                return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
            return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(prepare_error_response("No data found for this ID"), status=status.HTTP_400_BAD_REQUEST)

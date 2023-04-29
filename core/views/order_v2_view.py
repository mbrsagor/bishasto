from django.conf import settings
from django.core.mail import send_mail
from rest_framework import views, status, generics
from rest_framework.response import Response

from core.serializers import  order_v2_serializer
from core.models.order import Order
from utils import message, response

class CreateOrderAPIView(views.APIView):
    """
    Name: User can crate order.
    URL: /api/v1/catalogue/create-order/
    method: POST
    """

    def post(self, request, *args, **kwargs):
        try:
            # filter product ID from cart
            products = Cart.objects.filter(user=self.request.user)
            order_items = []
            for product in products:
                # Add cart items to OrderItem list
                order_item = OrderItem.objects.create(
                    product_id=product.product_id,
                    product_name=product.product_name,
                    product_price=product.product.price,
                    product_size=product.size,
                    product_color=product.color,
                    product_quantity=product.quantity,
                    product_thumbnail=product.product.feature,
                )
                order_items.append(order_item)
                order_item.save()

            # Create new order
            order = Order.objects.create(
                customer_id=self.request.user.id,
                status=request.data.get('status'),
                payment_id=request.data.get('payment'),
                full_name=request.data.get('full_name'),
                address=request.data.get('address'),
                phone_number=request.data.get('phone_number'),
                invoice_number=f"#Inv{order_item.product_id}"
            )
            order.order_item.add(*order_items)
            # Send mail to admin, agents, and consumer
            # agent_email = Cart.objects.get(id=self.request.user).product.store.owner.email
            send_mail(message.ORDER_CREATED,
                      message.ORDER_CONFIRM,
                      settings.EMAIL_HOST,
                      [self.request.user.email, settings.DEFAULT_ADMIN_EMAIL],
                      fail_silently=True
                      )
            # After adding products cart items delete
            products.delete()
            return Response(response.prepare_create_success_response(message.ORDER_CREATED),
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(response.prepare_error_response(str(ex)), status=status.HTTP_200_OK)


class OrderHistoryListViewAPI(generics.ListAPIView):
    """
    Name: My order history API
    Desc: user all order history with pagination
    URL: /api/v1/catalogue/order-history/
    method: Get
    """
    queryset = Order.objects.all()
    serializer_class = order_v2_serializer.OrderListSerializer

    # def get_queryset(self):
    #     return Order.objects.filter(customer=self.request.user)

    def list(self, request, *args, **kwargs):
        order = Order.objects.filter(customer=self.request.user)
        serializer = order_v2_serializer.OrderListSerializer(order, many=True)
        # Calculation price
        prices = []
        for data in serializer.data:
            items = data['order_item']
            for item in items:
                prices.append(int(item['product_total_price']))
        total_price = prices
        resp = {
            "message": message.DATA_RETURN,
            # "orderTotalPrice": sum(total_price),
            "data": serializer.data
        }
        return Response(resp, status=status.HTTP_200_OK)

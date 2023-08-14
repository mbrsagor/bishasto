import stripe
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import generics, status, views

from utils import response, messages
from catalogue.api.serializers import order_serializer
from paginations.common_pagination import CommonPagination
from catalogue.models.order import Order, Payment, Cart, OrderItem


class PaymentListView(generics.ListAPIView):
    """
    Name: payment get way listview
    URL: /api/v1/catalogue/payments/
    Method: GET
    """
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = order_serializer.PaymentSerializer
    pagination_class = CommonPagination


class CreateOrderAPIView(views.APIView):
    """
    Name: User can crate order.
    URL: /api/v1/catalogue/create-order/
    method: POST
    """

    def post(self, request, *args, **kwargs):

        stripe.api_key = settings.STRIPE_SECRET_KEY

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
                invoice_number=f"#Inv{order_item.id}"
            )
            order.order_item.add(*order_items)
            # Stripe Payment
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL
            )
            # Send mail to admin, agents, and consumer
            # agent_email = Cart.objects.get(id=self.request.user).product.store.owner.email
            send_mail(messages.ORDER_CREATED,
                      messages.ORDER_CONFIRM,
                      settings.EMAIL_HOST,
                      [self.request.user.email, settings.DEFAULT_ADMIN_EMAIL],
                      fail_silently=True
                      )
            # After adding products cart items delete
            products.delete()
            return Response(response.prepare_create_success_response(messages.ORDER_CREATED),
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
    serializer_class = order_serializer.OrderListSerializer
    pagination_class = CommonPagination

    def list(self, request, *args, **kwargs):
        order = Order.objects.filter(customer=self.request.user)
        serializer = order_serializer.OrderListSerializer(order, many=True)
        return Response(response.prepare_success_list_response(messages.DATA_RETURN, serializer.data),
                        status=status.HTTP_200_OK)

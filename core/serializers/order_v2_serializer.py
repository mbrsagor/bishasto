from rest_framework import serializers

from catalogue.models.order import Order, Payment, OrderItem


class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment method serializer
    """

    class Meta:
        model = Payment
        fields = (
            'id', 'name', 'photo', 'is_active'
        )


class OrderItemSerializer(serializers.ModelSerializer):
    """
    The serializer is a child order item serializer
    """

    class Meta:
        model = OrderItem
        fields = (
            'product_id', 'product_name', 'product_price',
            'product_quantity', 'product_size', 'product_color',
            'product_total_price', 'product_thumbnail'
        )


class OrderListSerializer(serializers.ModelSerializer):
    """
    Order list serializer
    """
    order_item = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id', 'order_status', 'payment_type', 'created_at',
            'invoice_number', 'order_ide', 'order_item'
        )

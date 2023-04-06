from rest_framework import serializers

from core.models.order import Order, OrderItem
from core.serializers.item_serializer import ItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer
    """
    class Meta:
        model = Order
        read_only_fields = ('user',)
        fields = [
            'id',
            'user',
            'item',
            'is_complete',
            'quantity',
            'shop_name',
            'total_price',
            'owner_price',
            'commission_price',
            'created_at',
            'updated_at'
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['item'] = ItemSerializer(instance.item_name).data
        return response


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Name: Order item serializer
    """
    class Meta:
        depth = 2
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('customer',)


class CreateOrderItemSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True).data

    class Meta:
        model = OrderItem
        read_only_fields = ('customer',)
        fields = [
            'id',
            'customer',
            'orders',
            'delivery_charge',
            'address',
            'transition_id',
            'phone_number',
            'reference',
            'payment_type',
            'status',
            'created_at',
            'updated_at'
        ]

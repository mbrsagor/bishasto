from rest_framework import serializers

from core.models.order import Order, OrderItem
from core.serializers.item_serializer import ItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        read_only_fields = ('user',)
        fields = [
            'id',
            'user',
            'item_name',
            'shop_name',
            'quantity',
            'total_price',
            'owner_price',
            'commission_price',
            'created_at',
            'updated_at'
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['item_name'] = ItemSerializer(instance.item_name).data
        return response


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('customer',)

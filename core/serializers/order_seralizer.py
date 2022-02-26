from rest_framework import serializers

from core.models.order import Order
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
            'status',
            'reference',
            'quantity',
            'address',
            'phone_number',
            'transition_id',
            'payment_type',
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


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        read_only_fields = ('user',)
        fields = [
            'id',
            'item_name',
            'status'
        ]

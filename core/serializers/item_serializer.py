from rest_framework import serializers
from core.models.item import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        read_only_fields = ('proprietor',)
        fields = (
            'id', 'item_name', 'item_category', 'tags', 'is_available', 'price', 'proprietor',
            'discount_price', 'commission', 'short_description', 'model',
            'item_type', 'created_at', 'updated_at', 'item_image'
        )

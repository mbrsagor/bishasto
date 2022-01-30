from rest_framework import serializers
from core.models.shop import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        read_only_fields = ('owner',)
        fields = [
            'id', 'owner', 'shop_name', 'shop_location', 'location_humanity', 'current_shop_age',
            'is_available', 'tread_license', 'address', 'shop_created_date', 'owner_humanity',
            'phone_number', 'documents', 'shop_image', 'created_at', 'updated_at'
        ]

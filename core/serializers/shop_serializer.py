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

    """
        def get_averageRating(self, obj):
        get_ratings = []
        product_rating = ProductRating.objects.filter(product=obj)
        ratings = ProductRatingSerializer(product_rating, many=True).data
        # put only rating number
        for rating in ratings:
            get_ratings.append(rating['rating'])
        result = sum(get_ratings) / len(get_ratings)
        return int(result)
    """
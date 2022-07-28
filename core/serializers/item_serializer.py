from rest_framework import serializers

from core.models.item import Item
from core.models.category import Tag
from core.serializers.category_serializer import CategorySerializer, TagSerializer


class ItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    def get_or_create_tag(self, tags):
        tag_ids = []
        for tag in tags:
            tag_instance, create = Tag.objects.get_or_create(pk=tag.get('id'), defaults=tag)
            tag_ids.append(tag_instance.pk)
        return tag_ids

    def create_or_update_tag(self, tags):
        tag_ids = []
        for tag in tags:
            tag_instance, create = Tag.objects.update_or_create(pk=tag.get('id'), defaults=tag)
            tag_ids.append(tag_instance.pk)
        return tag_ids

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        item = Item.objects.create(**validated_data)
        item.tags.set(self.get_or_create_tag(tags))
        return item

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        instance.tags.set(self.create_or_update_tag(tags))
        return instance

    class Meta:
        model = Item
        read_only_fields = ('proprietor',)
        fields = (
            'id', 'item_name', 'category', 'tags', 'is_available', 'price', 'proprietor',
            'discount_price', 'commission', 'short_description', 'model', 'item_type',
            'created_at', 'updated_at', 'item_image', 'galley_image2', 'galley_image3'
        )

    def validate_item_name(self, value):
        if len(value) <= 3:
            raise serializers.ValidationError("Item name should be more than 2 characters")
        return value

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['item_category'] = CategorySerializer(instance.item_category).data
        return response

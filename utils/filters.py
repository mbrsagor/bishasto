from django_filters import rest_framework as filters

from core.models.order import Order
from utils.enum import PROGRESS


class OrderFilter(filters.FilterSet):
    phone_number = filters.CharFilter(field_name='phone_number')
    transition_id = filters.CharFilter(field_name='transition_id')
    status = filters.ChoiceFilter(field_name='status', choices=PROGRESS.order_status())

    class Meta:
        model = Order
        fields = [
            'phone_number', 'transition_id', 'status'
        ]

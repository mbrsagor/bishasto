from django_filters import rest_framework as filters

from core.models.order import Order, OrderItem
from utils.enum_utils import PROGRESS


class OrderFilter(filters.FilterSet):
    """
    Order filter
    """
    item_name = filters.ModelChoiceFilter(field_name='item_name', queryset=Order.objects.all())
    is_complete = filters.BooleanFilter(field_name='is_complete')

    class Meta:
        model = Order
        fields = [
            'item_name', 'is_complete'
        ]


class OrderItemFilter(filters.FilterSet):
    """
    Order item filter
    """
    phone_number = filters.CharFilter(field_name='phone_number')
    transition_id = filters.CharFilter(field_name='transition_id')
    status = filters.ChoiceFilter(field_name='status', choices=PROGRESS.order_status())

    class Meta:
        model = OrderItem
        fields = [
            'phone_number', 'transition_id', 'status'
        ]

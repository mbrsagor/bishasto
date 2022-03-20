from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views.category_view import CategoryViewSet
from core.views.service_view import ServiceViewSet, ScheduleViewSet
from core.views.item_view import ItemAPIView, ItemUpdateDetailDeleteAPIView
from core.views.location_view import LocationViewSet
from core.views.shop_view import ShopProfileAPIView, ShopProfileUpdateDelete
from core.views.order_view import OrderCreateListAPIView, OrderStatusUpdateDetailsAPIView, OrderFilterListView
from core.views.order_item_view import OrderItemCreateAPIView, CreateOrderItemView, OrderItemFilterListView, \
    OrderItemDetailUpdateDeleteView
from core.views.preference_view import SiteSettingCreateListView, PreferenceCreateListView

router = DefaultRouter()
router.register('location', LocationViewSet)
router.register('category', CategoryViewSet)
router.register('service', ServiceViewSet)
router.register('schedule', ScheduleViewSet)

urlpatterns = [
    # Item
    path('item/', ItemAPIView.as_view(), name='item_view'),
    path('item/edit/<pk>/', ItemUpdateDetailDeleteAPIView.as_view(), name='item_update'),
    path('item/detail/<pk>/', ItemUpdateDetailDeleteAPIView.as_view(), name='item_detail'),
    path('item/delete/<pk>/', ItemUpdateDetailDeleteAPIView.as_view(), name='item_delete'),
    # Shop
    path('shop/', ShopProfileAPIView.as_view(), name='my_shop'),
    path('shop/<pk>/', ShopProfileUpdateDelete.as_view(), name='shop_update_delete'),
    path('order/', OrderCreateListAPIView.as_view(), name='orders'),
    path('order/<pk>/', OrderStatusUpdateDetailsAPIView.as_view(), name='oder_update_details'),
    path('order-filter/', OrderFilterListView.as_view(), name='order_filter'),
    # Order item
    path('order-item/', OrderItemCreateAPIView.as_view(), name='order_item'),
    path('create-order/', CreateOrderItemView.as_view(), name='create_order'),
    path('orderitem/<pk>/', OrderItemDetailUpdateDeleteView.as_view(), name='orderItem_update_detail_delete'),
    path('orderitem-filter/', OrderItemFilterListView.as_view(), name='orderItem_filter'),
    path('site/', SiteSettingCreateListView.as_view(), name='site_create_list'),
    path('site/', SiteSettingCreateListView.as_view(), name='site_create_list'),
    path('update-preference/', PreferenceCreateListView.as_view(), name='update_preference'),
] + router.urls

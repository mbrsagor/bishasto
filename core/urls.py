from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import item_view
from core.views import shop_view
from core.views import order_view
from core.views import service_view
from core.views import location_view
from core.views import category_view
from core.views import order_item_view
from core.views import preference_view

router = DefaultRouter()
router.register('location', location_view.LocationViewSet)
router.register('category', category_view.CategoryViewSet)
router.register('service', service_view.ServiceViewSet)
router.register('schedule', service_view.ScheduleViewSet)

urlpatterns = [
    # Item
    path('item/', item_view.ItemAPIView.as_view()),
    path('item/edit/<pk>/', item_view.ItemUpdateDetailDeleteAPIView.as_view()),
    path('item/detail/<pk>/', item_view.ItemUpdateDetailDeleteAPIView.as_view()),
    path('item/delete/<pk>/', item_view.ItemUpdateDetailDeleteAPIView.as_view()),
    # Shop
    path('shop/', shop_view.ShopProfileAPIView.as_view()),
    path('shop/<pk>/', shop_view.ShopProfileUpdateDelete.as_view()),
    path('order/', order_view.OrderCreateListAPIView.as_view()),
    path('order/<pk>/', order_view. OrderStatusUpdateDetailsAPIView.as_view()),
    path('order-filter/', order_view.OrderFilterListView.as_view()),
    # Order item
    path('order-item/', order_item_view.OrderItemCreateAPIView.as_view()),
    path('create-order/', order_item_view.CreateOrderItemView.as_view()),
    path('orderitem/<pk>/', order_item_view.OrderItemDetailUpdateDeleteView.as_view()),
    path('orderitem-filter/', order_item_view.OrderItemFilterListView.as_view()),
    # preference
    path('site/', preference_view.SiteSettingCreateListView.as_view()),
    path('preference/<pk>/', preference_view.PreferenceUpdateView.as_view()),
] + router.urls

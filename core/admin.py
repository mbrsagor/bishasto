from django.contrib import admin
from core.models.location import Location
from core.models.category import Category, Tag
from core.models.shop import Shop
from core.models.item import Item
from core.models.order import Order, OrderItem
from core.models.service import Service, Schedule
from core.models.preference import SiteSetting, Preference

admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Service)
admin.site.register(Schedule)
admin.site.register(SiteSetting)
admin.site.register(Preference)
admin.site.register(Tag)

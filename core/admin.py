from django.contrib import admin
from core.models.location import Location
from core.models.category import Category
from core.models.shop import Shop
from core.models.item import Item
from core.models.order import Order
from core.models.service import Service

admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Service)

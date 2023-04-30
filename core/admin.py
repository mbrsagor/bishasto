from django.contrib import admin
from core.models.location import Location
from core.models.category import Category, Tag
from core.models.shop import Shop
from core.models.item import Item, Color
from core.models.order import Order, OrderItem
from core.models.service import Service, Schedule
from core.models.preference import SiteSetting, Preference

admin.site.register(
    Location, Category, Shop, Item,
    Order, Color, OrderItem, Service, Schedule,
    SiteSetting, Preference, Tag
)

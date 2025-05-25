from django.contrib import admin
from .models import Inventory, InventoryLanguage, InventoryTag, InventoryType

admin.site.register(Inventory)
admin.site.register(InventoryLanguage)
admin.site.register(InventoryTag)
admin.site.register(InventoryType)

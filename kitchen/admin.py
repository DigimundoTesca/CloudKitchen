from django.contrib import admin

from kitchen.models import ProcessedProduct, Warehouse


@admin.register(ProcessedProduct)
class AdminProcessedCartridge(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'ticket')
    ordering = ('-created_at',)


@admin.register(Warehouse)
class AdminWarehouse(admin.ModelAdmin):
    list_display = ('supply', 'status', 'quantity', 'waste', 'cost')


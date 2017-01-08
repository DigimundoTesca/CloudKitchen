from django.contrib import admin

from orders.models import SupplierOrderDetail, SupplierOrder


class OrderDetailInline(admin.TabularInline):
    model = SupplierOrderDetail
    extra = 1


@admin.register(SupplierOrder)
class AdminOrder(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'user_charge',)
    inlines = [OrderDetailInline, ]

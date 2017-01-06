from django.contrib import admin

from orders.models import CustomerOrderDetail, CustomerOrder


class CustomerOrderDetailInline(admin.TabularInline):
    model = CustomerOrderDetail
    extra = 1


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', )
    inlines = [CustomerOrderDetailInline, ]

from django.contrib import admin

from customers.models import CustomerOrder, CustomerOrderDetail, CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfile(admin.ModelAdmin):
    list_display = ('id', 'name')


class CustomerOrderDetailInline(admin.TabularInline):
    model = CustomerOrderDetail
    extra = 1


@admin.register(CustomerOrder)
class AdminCustomerOrder(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', )
    inlines = [CustomerOrderDetailInline, ]

from django.contrib import admin

from customers.models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'address', 'latitude', 'longitude')

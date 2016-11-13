# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)


class CashRegisterInline(admin.StackedInline):
    model = CashRegister
    extra = 2


@admin.register(BranchOffice)
class AdminBranchOffice(admin.ModelAdmin):
    list_display = ('name', 'manager', 'address',)
    inlines = [CashRegisterInline, ]


@admin.register(Provider)
class AdminProvider(admin.ModelAdmin):
    list_display = ('name', 'image',)


@admin.register(SuppliesCategory)
class AdminCSuppliesCategory(admin.ModelAdmin):
    list_display = ('name', 'image',)


@admin.register(SupplyLocation)
class AdminSupplLocation(admin.ModelAdmin):
    list_display = ('location', 'branch_office',)


@admin.register(Supply)
class AdminSupply(admin.ModelAdmin):
    list_display = ('name', 'category', 'provider', 'presentation_unit', 'measurement_unit', 'measurement_cost',)

    
class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'user_charge',)
    inlines = [OrderDetailInline, ]


class CartridgeRecipeInline(admin.TabularInline):
    model = CartridgeRecipe
    extra = 1
    

@admin.register(Cartridge)
class AdminCashRegister(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')
    inlines = [CartridgeRecipeInline, ]


class PackageCartridgeRecipeInline(admin.TabularInline):
    model = PackageCartridgeRecipe
    extra = 1


@admin.register(PackageCartridge)
class AdminPackageCartridge(admin.ModelAdmin):
    list_display = ('name', 'price', 'package_active',)
    inlines = [PackageCartridgeRecipeInline]


@admin.register(ProcessedCartridge)
class AdminProcessedCartridge(admin.ModelAdmin):
    list_display = ('name', 'status', 'cartridge_parent', 'package_cartridge_parent', 'created_at')


@admin.register(Warehouse)
class AdminWarehouse(admin.ModelAdmin):
    list_display = ('supply', 'status', 'quantity', 'waste', 'cost')


class TicketDetailInline(admin.TabularInline):
    model = TicketDetail
    extra = 1
    

@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    list_display = ('created_at', 'seller', 'cash_register',)
    inlines = [TicketDetailInline, ]


class CustomerOrderDetailInline(admin.TabularInline):
    model = CustomerOrderDetail
    extra = 1
    

@admin.register(CustomerOrder)
class AdminCustomerOrder(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', )
    inlines = [CustomerOrderDetailInline, ]

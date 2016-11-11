# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('user', 'phone_number',)


@admin.register(BranchOffice)
class AdminBranchOffice(admin.ModelAdmin):
    list_display = ('name', 'manager', 'address',)


@admin.register(CashRegister)
class AdminCashRegister(admin.ModelAdmin):
    list_display = ('code', 'status', 'branch_office',)


@admin.register(Provider)
class AdminProvider(admin.ModelAdmin):
    list_display = ('name', 'image',)


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'image',)


@admin.register(SupplyLocation)
class AdminSupplLocation(admin.ModelAdmin):
    list_display = ('location', 'branch_office',)


@admin.register(Supply)
class AdminSupply(admin.ModelAdmin):
    list_display = ('name', 'category', 'provider', 'presentation_unit', 'measurement_unit', 'measurement_cost',)


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'user_charge',)


@admin.register(OrderDetail)
class AdminOderDetail(admin.ModelAdmin):
    list_display = ('order', 'supply', 'quantity', 'cost',)


@admin.register(Cartridge)
class AdminCashRegister(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')


@admin.register(CartridgeRecipe)
class AdminCartridgeRecipe(admin.ModelAdmin):
    list_display = ('cartridge', 'supply', 'quantity',)


@admin.register(PackageCartridge)
class AdminPackageActive(admin.ModelAdmin):
    list_display = ('name', 'price', 'package_active',)


@admin.register(PackageCartridgeRecipe)
class AdminPackageCartridgeRecipe(admin.ModelAdmin):
    list_display = ('package_cartridge', 'cartridge', 'quantity',)


@admin.register(ProcessedCartridge)
class AdminProcessedCartridge(admin.ModelAdmin):
    list_display = ('name', 'status', 'cartridge_parent', 'package_cartridge_parent', 'created_at')


@admin.register(Warehouse)
class AdminWarehouse(admin.ModelAdmin):
    list_display = ('supply', 'status', 'quantity', 'waste', 'cost')


@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    list_display = ('created_at', 'seller', 'cash_register',)


@admin.register(TicketDetails)
class AdminTicketDetails(admin.ModelAdmin):
    list_display = ('ticket', 'cartridge', 'package_cartridge', 'quantity', 'price')


@admin.register(CustomerOrder)
class AdminCustomerOrder(admin.ModelAdmin):
    list_display = ('created_at', 'status',)


@admin.register(CustomerOrderDetail)
class AdminCustomerOrderDetails(admin.ModelAdmin):
    list_display = ('customer_order', 'cartridge', 'package_cartridge', 'quantity',)
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from supplies.models import SuppliesCategory, SupplyLocation, Supply, SupplierOrderDetail, SupplierOrder, \
    CartridgeRecipe, Cartridge, PackageCartridgeRecipe, ProcessedCartridge, PackageCartridge, Warehouse, TicketDetail, \
    Ticket


@admin.register(SuppliesCategory)
class AdminSuppliesCategory(admin.ModelAdmin):
    list_display = ('name', 'image',)


@admin.register(SupplyLocation)
class AdminSupplyLocation(admin.ModelAdmin):
    list_display = ('location', 'branch_office',)


@admin.register(Supply)
class AdminSupply(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'presentation_unit',  'presentation_cost', 'measurement_unit',
                    'measurement_quantity', )


class OrderDetailInline(admin.TabularInline):
    model = SupplierOrderDetail
    extra = 1


@admin.register(SupplierOrder)
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

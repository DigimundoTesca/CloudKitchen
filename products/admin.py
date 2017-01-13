# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from products.models import Warehouse, ProcessedCartridge, PackageCartridge, PackageCartridgeRecipe, \
    CartridgeRecipe, Supply, SupplyLocation, SuppliesCategory, Cartridge


@admin.register(SuppliesCategory)
class AdminSuppliesCategory(admin.ModelAdmin):
    list_display = ('name', 'image',)


@admin.register(SupplyLocation)
class AdminSupplyLocation(admin.ModelAdmin):
    list_display = ('location', 'branch_office',)


@admin.register(Supply)
class AdminSupply(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'presentation_unit', 'presentation_cost', 'measurement_unit',
                    'measurement_quantity',)
    ordering = ['name']


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


@admin.register(PackageCartridgeRecipe)
class AdminTicket(admin.ModelAdmin):
    list_display = ['package_cartridge', 'cartridge', 'quantity']


@admin.register(ProcessedCartridge)
class AdminProcessedCartridge(admin.ModelAdmin):
    list_display = ('name', 'status', 'cartridge_parent', 'package_cartridge_parent', 'created_at')


@admin.register(Warehouse)
class AdminWarehouse(admin.ModelAdmin):
    list_display = ('supply', 'status', 'quantity', 'waste', 'cost')


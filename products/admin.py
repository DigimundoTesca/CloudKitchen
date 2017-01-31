# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from products.models import PackageCartridge, PackageCartridgeRecipe, \
    CartridgeRecipe, Supply, SupplyLocation, SuppliesCategory, Cartridge


@admin.register(SuppliesCategory)
class AdminSuppliesCategory(admin.ModelAdmin):
    list_display = ('name', 'image',)


@admin.register(SupplyLocation)
class AdminSupplyLocation(admin.ModelAdmin):
    list_display = ('location', 'branch_office',)


@admin.register(Supply)
class AdminSupply(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'supplier', 'presentation_unit', 'presentation_cost', 'measurement_unit',
                    'measurement_quantity',)
    list_display_links = ('id', 'name')
    ordering = ['name']


class CartridgeRecipeInline(admin.TabularInline):
    model = CartridgeRecipe
    extra = 1


@admin.register(Cartridge)
class AdminCashRegister(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at')
    list_display_links = ('id', 'name')
    inlines = [CartridgeRecipeInline, ]


class PackageCartridgeRecipeInline(admin.TabularInline):
    model = PackageCartridgeRecipe
    extra = 1


@admin.register(PackageCartridge)
class AdminPackageCartridge(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'package_active',)
    list_display_links = ('id', 'name')
    inlines = [PackageCartridgeRecipeInline]

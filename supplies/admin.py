# coding=utf-8
from __future__ import unicode_literals
from django.contrib import admin
from .models import Supply, Category, Provider, StockChain, PackageCartridges, Cartridge


@admin.register(Provider)
class AdminProvider(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(Supply)
class AdminSupply(admin.ModelAdmin):
    list_display = ('name', 'category', 'barcode', 'provider', 'ideal_durability', 'image')


@admin.register(PackageCartridges)
class AdminPackageCartridges(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Cartridge)
class AdminCartridge(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(StockChain)
class AdminStockChain(admin.ModelAdmin):
    list_display = ('id', 'registered_at', 'expiry_date', 'supply', 'status', 'metric')

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Supply, Category, Provider, StockChain, PackageCartridges, Cartridge, Order, OrdersDetails, BranchOffice, CashRegister

@admin.register(BranchOffice)
class AdminBranchOffice(admin.ModelAdmin):
    list_display = ('name', 'addres')


@admin.register(Cartridge)
class AdminCartridge(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(CashRegister)
class AdminCashRegister(admin.ModelAdmin):
    list_display = ('id', 'code', 'status', 'branch_office')


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'expiry_date')


@admin.register(OrdersDetails)
class AdminOrdersDetails(admin.ModelAdmin):
    list_display = ('supply', 'order', 'metric', 'quantity', 'cost')


@admin.register(PackageCartridges)
class AdminPackageCartridges(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Provider)
class AdminProvider(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(StockChain)
class AdminStockChain(admin.ModelAdmin):
    list_display = ('id', 'registered_at', 'expiry_date', 'supply', 'status', 'metric')


@admin.register(Supply)
class AdminSupply(admin.ModelAdmin):
    list_display = ('name', 'category', 'barcode', 'provider', 'ideal_durability', 'image')



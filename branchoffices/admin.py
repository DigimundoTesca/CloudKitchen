from django.contrib import admin

from branchoffices.models import CashRegister, BranchOffice, Supplier


class CashRegisterInline(admin.StackedInline):
    model = CashRegister
    extra = 2


@admin.register(BranchOffice)
class AdminBranchOffice(admin.ModelAdmin):
    list_display = ('name', 'manager', 'address',)
    inlines = [CashRegisterInline, ]


@admin.register(Supplier)
class AdminProvider(admin.ModelAdmin):
    list_display = ('name', 'image',)

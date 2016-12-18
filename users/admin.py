from django.contrib import admin

from users.models import UserProfile, UserRol, CashRegister, BranchOffice, Supplier


class UserProfileAdmin(admin.ModelAdmin):
    pass


class UserRolAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserRol, UserRolAdmin)


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
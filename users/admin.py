from django.contrib import admin

from users.models import Profile, Rol, CashRegister, BranchOffice, Supplier


class UserProfileAdmin(admin.ModelAdmin):
    pass


class RolAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, UserProfileAdmin)
admin.site.register(Rol, RolAdmin)


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
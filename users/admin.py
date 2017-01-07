from django.contrib import admin

from users.models import Profile, Rol


class UserProfileAdmin(admin.ModelAdmin):
    pass


class RolAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, UserProfileAdmin)
admin.site.register(Rol, RolAdmin)

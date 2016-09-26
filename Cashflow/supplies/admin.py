from django.contrib import admin
from .models import Supply, Category, Provider

@admin.register(Provider)
class  AdminProvider(admin.ModelAdmin):
	list_display	= ('name' , 'image')

@admin.register(Category)
class  AdminCategory(admin.ModelAdmin):
	list_display	= ('name' , 'image')

@admin.register(Supply)
class  AdminSupply(admin.ModelAdmin):
	list_display	= ('name' , 'category', 'barcode', 'provider', 'image')
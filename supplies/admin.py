from django.contrib import admin
from .models import Supply, Category, Provider, StockChain, Metric

@admin.register(Provider)
class  AdminProvider(admin.ModelAdmin):
    list_display    = ('name' , 'image')


@admin.register(Category)
class  AdminCategory(admin.ModelAdmin):
    list_display    = ('name' , 'image')


@admin.register(Supply)
class  AdminSupply(admin.ModelAdmin):
    list_display    = ('name' , 'category', 'barcode', 'provider', 'ideal_durability', 'image')


@admin.register(Metric)
class  AdminMetric(admin.ModelAdmin):
    list_display    = ('metric_type', 'stock', 'parent_metric')


@admin.register(StockChain)
class  AdminStockChain(admin.ModelAdmin):
    list_display    = ('id' , 'registered_at', 'expiry_date', 'supply', 'status', 'metric')
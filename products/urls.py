from django.conf.urls import url

from products import views

app_name = 'products'

urlpatterns = [
    # test
    url(r'^test/$', views.test, name='test'),

    # Supplies
    url(r'^supplies/$', views.supplies, name='supplies'),
    url(r'^supplies/new/$', views.new_supply, name='new_supply'),
    url(r'^supplies/(?P<pk>[0-9]+)/$', views.supply_detail, name='supply_detail'),

    # Suppliers
    url(r'^suppliers/$', views.suppliers, name='suppliers'),

    # Categories
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^categories/new/$', views.new_category, name='new_category'),
    url(r'^categories/([A-Za-z]+)/$', views.categories_supplies, name='categories_supplies'),

    # Cartridges
    url(r'^cartridges/$', views.cartridges, name='cartridges'),
    url(r'^cartridges/new/$', views.new_cartridge, name='new_cartridge'),
]
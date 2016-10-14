from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    # Supplies
    url(r'^login/$', views.login, name = 'views.login'),
    url(r'^supplies/$', views.supplies, name='views.supplies'),
    url(r'^supplies/new/$', views.new_supply, name='views.new_supply'),
    url(r'^supplies/(?P<pk>[0-9]+)/$', views.supply_detail, name='views.supply_detail'),

    # Categories
    url(r'^categories/$', views.categories, name='views.categories'),
    url(r'^categories/new/$', views.new_category, name='views.new_category'),
    url(r'^categories/([A-Za-z]+)/$', views.categories_supplies, name='views.categories_supplies'),

    # Cartridges
    # url(r'^cartridges/$', views.cartridges, name='views.cartridges'),

    # Providers
    url(r'^providers/$', views.providers, name='views.providers'),
]
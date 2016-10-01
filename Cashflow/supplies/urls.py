from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^login/$', views.login, name = 'views.login'),
    url(r'^supplies/$', views.supplies, name='views.supplies'),
    url(r'^supplies/new/$', views.new_supply, name='views.new_supply'),
    url(r'^supplies/(?P<pk>[0-9]+)/$', views.supply_detail, name='views.supply_detail'),

    url(r'^categories/$', views.categories, name='views.categories'),
    url(r'^categories/([A-Za-z]+)/$', views.categories_supplies, name='views.categories_supplies'),
]
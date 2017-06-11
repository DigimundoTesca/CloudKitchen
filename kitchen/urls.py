from django.conf.urls import url

from kitchen import views

app_name = 'kitchen'

urlpatterns = [
    # Warehouse
    # url(r'warehouse/$', views.supplies, name='supplies'),

    # Kitchen
    url(r'kitchen/1/$', views.cold_kitchen, name='kitchen_2'),
    url(r'kitchen/2/$', views.hot_kitchen, name='kitchen_1'),
    url(r'kitchen/assembly/$', views.assembly, name='assembly'),
]

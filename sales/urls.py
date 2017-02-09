from django.conf import settings
from django.conf.urls import url

from sales import views

app_name = 'sales'

urlpatterns = [
    # sales
    url(r'^sales/$', views.sales, name='sales'),
    url(r'^sales/new/$', views.new_sale, name='new_sale'),
    url(r'^sales/sales-day/$', views.get_sales_day_view, name='get_sales_day'),
]

if settings.DEBUG:
    urlpatterns.append(url('^sales/test/$', views.test, name='test'))


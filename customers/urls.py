from django.conf.urls import url

from . import views

app_name = 'customers'

urlpatterns = [
    # New Customer
    url(r'^register/$', views.new_customer, name='new_customer'),
    url(r'^thanks/$', views.thanks, name='thanks'),

    # Customer orders
    url(r'^customers/orders/$', views.customer_orders, name='new_customer_order'),
    url(r'^customers/orders/new/$', views.new_customer_order, name='new_customer_order'),

]

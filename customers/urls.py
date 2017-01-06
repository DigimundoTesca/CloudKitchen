from django.conf.urls import url

from . import views

app_name = 'customers'

urlpatterns = [
    # New Customer
    url(r'^register/$', views.new_customer, name='new_customer'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^register/list$', views.customers_list, name='customers_list'),
]

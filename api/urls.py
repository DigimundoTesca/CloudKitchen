from django.conf.urls import url
from . import views


customer_orders = views.CustomerOrderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

customer_order_detail = views.CustomerOrderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
   url(r'^v1/customer-orders/$', customer_orders, name='customer_orders_list'),
   url(r'^v1/customer-orders/(?P<pk>[0-9]+)/$', customer_order_detail, name='customer_order_detail'),
]
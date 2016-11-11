from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^orders/$', CustomerOrderList.as_view(), name='orderslists'),
]
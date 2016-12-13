from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from api.serializers import CustomerOrderSerializer, CustomerOrderDetailSerializer, CustomerOrderStatusSerializer, \
    CustomerOrderScoreSerializer
from supplies.models import CustomerOrder, CustomerOrderDetail


class CustomerOrderViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()
    serializer_class = CustomerOrderSerializer


class CustomerOrderStatusViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()
    serializer_class = CustomerOrderStatusSerializer


class CustomerOrderScoreViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()
    serializer_class = CustomerOrderScoreSerializer

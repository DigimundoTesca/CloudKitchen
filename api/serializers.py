from rest_framework import serializers
from supplies.models import CustomerOrder, CustomerOrderDetail


class CustomerOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrderDetail
        fields = ('cartridge', 'package_cartridge', 'quantity')


class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrder
        fields = ('id', 'created_at', 'delivery_date', 'customer', 'status', 'price', 'latitude', 'longitude',)

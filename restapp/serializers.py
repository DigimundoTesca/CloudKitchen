from supplies.models import CustomerOrder
from rest_framework import serializers


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerOrder
        fields = ('id', 'latitude', 'longitude', 'price')
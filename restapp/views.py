from rest_framework import generics
from supplies.models import *
from .serializers import PlaceSerializer
from django.shortcuts import get_object_or_404


class CustomerOrderList(generics.ListCreateAPIView):
    queryset = CustomerOrder.objects.all()
    serializer_class = PlaceSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk=self.kwargs['pk'],
        )
        return obj


class CustomerOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerOrder.objects.all()
    serializer_class = PlaceSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk=self.kwargs['pk'],
        )
        return obj
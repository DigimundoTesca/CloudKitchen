# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from supplies.models import Supply, SuppliesCategory, Cartridge, CustomerOrder, CustomerOrderDetail


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = '__all__'


class SuppliesCategoryForm(forms.ModelForm):
    class Meta:
        model = SuppliesCategory
        fields = '__all__'


class CartridgeForm(forms.ModelForm):
    class Meta:
        model = Cartridge
        fields = '__all__'


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = '__all__'


class CustomerOrderDetailForm(forms.ModelForm):
    class Meta:
        model = CustomerOrderDetail
        fields = '__all__'

from django import forms

from customers.models import CustomerOrder, CustomerOrderDetail


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = '__all__'


class CustomerOrderDetailForm(forms.ModelForm):
    class Meta:
        model = CustomerOrderDetail
        fields = '__all__'

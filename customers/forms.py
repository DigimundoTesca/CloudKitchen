from django import forms
from customers.models import CustomerOrder, CustomerOrderDetail, CustomerProfile

from functools import partial


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomerOrderForm, self).__init__(*args, **kwargs)
        self.fields['delivery_date'].widget.attrs.update({'class': 'flatpickr'})


class CustomerOrderDetailForm(forms.ModelForm):
    class Meta:
        model = CustomerOrderDetail
        fields = '__all__'


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)
        self.fields['longitude'].widget.attrs.update({'class': 'text-hide'})
        self.fields['latitude'].widget.attrs.update({'class': 'text-hide'})

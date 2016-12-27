from django import forms
from django.contrib.admin import widgets

from customers.models import CustomerOrder, CustomerOrderDetail

from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


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

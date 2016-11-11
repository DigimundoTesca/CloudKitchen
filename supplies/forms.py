# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import *


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class CartridgeForm(forms.ModelForm):
    class Meta:
        model = Cartridge
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

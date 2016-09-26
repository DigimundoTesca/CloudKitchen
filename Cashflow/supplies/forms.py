from django import forms
from .models import Supply, Category, Provider

class SupplyForm(forms.ModelForm):
	class Meta:
		model = Supply
		fields = ('__all__')

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ('__all__')
	
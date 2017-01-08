from django import forms
from django.contrib.auth.models import User

from users.models import User as UserProfile, CustomerProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'phone_number']


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['user', 'longitude', 'latitude', 'address', 'first_dabba']



from django import forms

from users.models import User as UserProfile


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number',]

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True)
    aadhar = forms.ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'aadhar', 'password1', 'password2']
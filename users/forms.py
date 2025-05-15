from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    college_id = forms.IntegerField(
        min_value=1000,
        max_value=9999,
        required=True,
        help_text="Enter your 4-digit College ID"
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms.widgets import ClearableFileInput

# Common styles
COMMON_INPUT_STYLE = (
    'width: 100%; '
    'margin: 0.5em 0; '
    'border: 1px solid #444; '
    'border-radius: 8px; '
    'background: #2a2a3d; '
    'color: #fff; '
    'padding: 0.75em 1em; '
    'box-sizing: border-box;'
)

COMMON_TEXTAREA_STYLE = (
    'width: 100%; '
    'margin: 0.5em 0; '
    'border: 1px solid #444; '
    'border-radius: 12px; '
    'background: #2a2a3d; '
    'color: #fff; '
    'padding: 0.75em 1em; '
    'box-sizing: border-box; '
    'resize: vertical;'
)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Enter your username',
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'password1': 'Enter your password',
            'password2': 'Confirm your password',
            'college_id': 'Enter your 4-digit College ID',
        }
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'style': COMMON_TEXTAREA_STYLE,
                    'placeholder': placeholders.get(name, '')
                })
            else:
                field.widget.attrs.update({
                    'style': COMMON_INPUT_STYLE,
                    'placeholder': placeholders.get(name, '')
                })


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Enter your username',
            'password': 'Enter your password',
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'style': COMMON_INPUT_STYLE,
                'placeholder': placeholders.get(name, '')
            })


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'users/custom_clearable_file_input.html'


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    college_id = forms.IntegerField(
        min_value=1000,
        max_value=9999,
        required=True,
        help_text="Enter your 4-digit College ID"
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=CustomClearableFileInput,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'college_id': 'Enter your 4-digit College ID',
        }
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'style': COMMON_TEXTAREA_STYLE,
                    'placeholder': placeholders.get(name, '')
                })
            else:
                field.widget.attrs.update({
                    'style': COMMON_INPUT_STYLE,
                    'placeholder': placeholders.get(name, '')
                })


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'old_password': 'Enter your old password',
            'new_password1': 'Enter new password',
            'new_password2': 'Confirm new password',
        }
        for fieldname in ['new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None  # Remove default help text
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'style': COMMON_INPUT_STYLE,
                'placeholder': placeholders.get(name, '')
            })

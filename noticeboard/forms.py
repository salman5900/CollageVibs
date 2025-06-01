from django import forms
from .models import Noticeboard
from django.forms.widgets import ClearableFileInput

class CustomClear(ClearableFileInput):
    template_name = 'noticeboard/clearablefile.html'
class NoticeboardForm(forms.ModelForm):
    class Meta:
        model = Noticeboard
        fields = ['title', 'image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': (
                    'width: 100%; '
                    'margin: 0.5em 0; '
                    'border: 1px solid #444; '
                    'border-radius: 8px; '
                    'background: #2a2a3d; '
                    'color: #fff; '
                    'padding: 0.75em 1em; '
                    'box-sizing: border-box;'
                ),
                'placeholder': 'Enter title',
            }),
            'image': CustomClear(attrs={
                'class': 'form-control',
                'style': (
                    'width: 100%; '
                    'margin: 0.5em 0; '
                    'border: 1px solid #444; '
                    'border-radius: 8px; '
                    'background: #2a2a3d; '
                    'color: #fff; '
                    'padding: 0.75em 1em; '
                    'box-sizing: border-box;'
                ),
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'style': (
                    'width: 100%; '
                    'margin: 0.5em 0; '
                    'border: 1px solid #444; '
                    'border-radius: 12px; '
                    'background: #2a2a3d; '
                    'color: #fff; '
                    'padding: 0.75em 1em; '
                    'box-sizing: border-box; '
                    'resize: vertical;'
                ),
                'placeholder': 'Write your notice here...',
            }),
        }

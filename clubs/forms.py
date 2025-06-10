# forms.py
from django import forms
from .models import Club

class ClubCreateForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
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
                'placeholder': 'Enter Name of the Club',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 13,
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
                'placeholder': 'Write your Discription for the Club here...',
            }),
        }


from django.forms import ModelForm
from django import forms
from .models import GlobalChatMessage

class GlobalChatCreateForm(ModelForm):
    class Meta:
        model = GlobalChatMessage
        fields = ['message']
        widgets = {
        'message': forms.TextInput(attrs={ 
            'placeholder': 'Add message  ...',
            'maxlength': '300',
            'autofocus': True,
    }),
}


from django.forms import ModelForm, TextInput
from .models import GroupMessage


class GroupMessageForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ('body', )
        widgets = {
            'body': TextInput(attrs={
                'class': 'w-full',
                'placeholder': 'Add message ...',
                'maxlength': 150
            })
        }

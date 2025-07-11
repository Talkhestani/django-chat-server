from django import forms
from django.forms import ModelForm, TextInput
from .models import ChatGroup, GroupMessage


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


class NewGroupFrom(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ('chat_name', )
        widgets = {
            'chat_name': forms.TextInput(attrs={
                'placeholder': 'Add Name ...',
                'class': 'p-4 text-black',
                'maxlength': '300',
                'autofocus': True
            })
        }

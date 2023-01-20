from django import forms
from .models import UserPc

class PCForms(forms.ModelForm):
    class Meta:
        model = UserPc
        fields = ('name', 'ip', 'mac_adress', 'description')
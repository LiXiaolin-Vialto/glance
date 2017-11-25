from django import forms
from django.contrib.auth.models import User
from .models import Serial


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class SerialForm(forms.ModelForm):
    class Meta:
        model = Serial
        fields = ('serial', 'name', 'moblie')

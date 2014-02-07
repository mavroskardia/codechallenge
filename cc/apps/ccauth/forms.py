from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Your name','class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your password','class':'form-control'}))

from django import forms
from django.forms import ModelForm

from .models import Coder


class ProfileForm(ModelForm):
	name = forms.CharField(
		required=False,
		widget=forms.TextInput(
			attrs={
			'placeholder': 'What do you want to be called instead of your username?',
			'maxlength': 256,
			'size': 50,
			'class': 'form-control'
			}))

	tagline = forms.CharField(
		required=False,
		widget=forms.TextInput(
			attrs={
			'placeholder': 'Your motto in life, perhaps?',
			'maxlength': 256,
			'size': 50,
			'class': 'form-control'
			}))

	about = forms.CharField(
		required=False,
		widget=forms.Textarea(
			attrs={
			'placeholder': 'What do you want people to know about you?',
			'class': 'form-control'
			}))

	class Meta:
		model = Coder
		fields = ['name', 'tagline', 'about']

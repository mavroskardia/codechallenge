from django import forms
from django.forms import ModelForm

from .models import Challenge
from .models import Rule


class ChallengeForm(ModelForm):
	class Meta:
		model = Challenge

	name = forms.CharField(
		required=True,
		widget=forms.TextInput(
			attrs={
			'placeholder': 'What is the name of this challenge?',
			'maxlength': 256,
			'size': 50,
			'class': 'form-control'
			}))

	duration = forms.CharField(
		required=True,
		widget=forms.TextInput(
			attrs={
			'placeholder': 'How long, in days, does this Challenge last? (ex. 30)',
			'maxlength': 3,
			'size': 5,
			'class': 'form-control'
			}))

class RuleForm(ModelForm):
	description = forms.CharField(required=True)

	class Meta:
		model = Rule
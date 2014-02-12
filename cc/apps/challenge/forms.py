from django import forms
from django.forms import ModelForm

from .models import Challenge
from .models import Rule


class ChallengeForm(ModelForm):
	name = forms.CharField(required=True)
	duration = forms.CharField(required=True)
	class Meta:
		model = Challenge

class RuleForm(ModelForm):
	description = forms.CharField(required=True)
	class Meta:
		model = Rule
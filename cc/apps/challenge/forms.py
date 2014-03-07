from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Challenge
from .models import Rule


class ChallengeForm(ModelForm):
	name = forms.CharField(required=True)
	duration = forms.CharField(required=True)
	class Meta:
		model = Challenge

AddRuleFormset = inlineformset_factory(Challenge, Rule, can_delete=False, extra=1)

#class RuleForm(ModelForm):
#	description = forms.CharField(required=True)
#	class Meta:
#		model = Rule
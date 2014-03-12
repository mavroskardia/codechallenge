from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Challenge, Rule, ChallengeComment


AddRuleFormset = inlineformset_factory(Challenge, Rule, can_delete=False, extra=0)
AddRuleTemplateFormset = inlineformset_factory(Challenge, Rule, can_delete=False, extra=1)

class ChallengeForm(ModelForm):
	class Meta:
		model = Challenge
		fields = ('name', 'duration',)

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


class ChallengeCommentForm(ModelForm):
	class Meta:
		model = ChallengeComment
		fields = ('text',)

	text = forms.CharField(
		required=True,
		widget=forms.Textarea(
			attrs={
			'placeholder': 'What is your comment?',
			'rows': 2,
			'cols': 40,
			'class': 'form-control'
			}))

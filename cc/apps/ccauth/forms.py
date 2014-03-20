import re

from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Your name','class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your password','class':'form-control'}))

class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Your name','class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your password','class':'form-control'}))
	confirmpassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder':'Confirm your password','class':'form-control'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Your email address','class':'form-control'}))
	confirmemail = forms.EmailField(label='Confirm Email', widget=forms.TextInput(attrs={'placeholder':'Confirm your email address','class':'form-control'}))

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		confirmpassword = cleaned_data.get('confirmpassword', '')
		email = cleaned_data.get('email', '')
		confirmemail = cleaned_data.get('confirmemail', '')

		if password != confirmpassword:
			self._errors['password'] = self.error_class([u'Password confirmation and password do not match.'])
			del cleaned_data['password']
			del cleaned_data['confirmpassword']

		if email != confirmemail:
			self._errors['email'] = self.error_class([u'Email confirmation and email do not match.'])
			del cleaned_data['email']
			del cleaned_data['confirmemail']

		if re.search('\W', username):
			self._errors['username'] = self.error_class([u'Username cannot have whitespace'])

		return cleaned_data
from django import forms


class ProfileForm(forms.Form):
	name = forms.CharField(
		required=False,
		widget=forms.TextInput(
			attrs={
			'placeholder': 'What do you want to be called instead of your username?',
			'maxlength': 256,
			'size': 50,
			}))

	tagline = forms.CharField(
		required=False,
		widget=forms.TextInput(
			attrs={
			'placeholder': 'Your motto in life, perhaps?',
			'maxlength': 256,
			'size': 50,
			}))

	about = forms.CharField(
		required=False,
		widget=forms.Textarea(attrs={'placeholder': 'What do you want people to know about you?'}))

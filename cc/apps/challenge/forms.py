import zipfile

from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Challenge, Rule, ChallengeComment, Entry, EntryComment, EntryScreenshot


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


class RuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = ('description', )

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
            'class': 'form-control',
            'rows': 2,
            'cols': 20,
            'placeholder': 'Describe this rule'
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
            'cols': 20,
            'class': 'form-control'
            }))


class SubmitEntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ('name', 'description', 'thefile', )

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Name of your entry'
        }))

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
            'class': 'form-control',
            'rows': 2,
            'cols': 20,
            'placeholder': 'Describe your entry'
        }))

    def clean(self):
        cleaned_data = super(SubmitEntryForm, self).clean()
        thefile = cleaned_data.get('thefile')

        if not zipfile.is_zipfile(thefile.file):
            self._errors['thefile'] = self.error_class([u'Submission is not a valid zip file.'])
            del cleaned_data['thefile']

        return cleaned_data


class SubmitEntryCommentForm(ModelForm):
    class Meta:
        model = EntryComment
        fields = ('text',)

    text = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
            'placeholder': 'What is your comment?',
            'rows': 2,
            'cols': 20,
            'class': 'form-control'
            }))

class SubmitEntryScreenshotForm(ModelForm):
    class Meta:
        model = EntryScreenshot
        fields = ('pic',)

    pic = forms.FileField(label='Your screenshot:')


AddRuleFormset = inlineformset_factory(Challenge, Rule, can_delete=False, extra=0)
AddRuleTemplateFormset = inlineformset_factory(Challenge, Rule, form=RuleForm, can_delete=False, extra=1)

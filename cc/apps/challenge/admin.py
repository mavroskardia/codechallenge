from django.contrib import admin
from django.forms import Textarea
from django.db import models

from .models import Challenge, Rule, Participant, ChallengeComment, Submission


class RuleInline(admin.TabularInline):
	model = Rule
	formfield_overrides = {
		models.TextField: { 'widget': Textarea(attrs={ 'rows': 2, 'cols': 40 }) }
	}

class ParticipantInline(admin.TabularInline):
	model = Participant
	readonly_fields = ('is_owner',)

class ChallengeCommentInline(admin.TabularInline):
	model = ChallengeComment
	formfield_overrides = {
		models.TextField: { 'widget': Textarea(attrs={ 'rows': 2, 'cols': 40 }) }
	}

class SubmissionInline(admin.TabularInline):
	model = Submission

class ChallengeAdmin(admin.ModelAdmin):
	fields = ('name', 'duration', 'owner',)
	inlines = [RuleInline, ParticipantInline,ChallengeCommentInline,SubmissionInline]

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Participant)
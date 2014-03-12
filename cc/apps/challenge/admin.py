from django.contrib import admin

from .models import Challenge, Rule, Participant


class RuleInline(admin.StackedInline):
	model = Rule

class ParticipantInline(admin.StackedInline):
	model = Participant
	readonly_fields = ('is_owner',)

class ChallengeAdmin(admin.ModelAdmin):
	fields = ('name', 'duration', 'owner',)
	inlines = [RuleInline, ParticipantInline,]

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Participant)
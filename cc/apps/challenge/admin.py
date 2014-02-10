from django.contrib import admin

from .models import Challenge, Rule


class RuleInline(admin.StackedInline):
	model = Rule

class ChallengeAdmin(admin.ModelAdmin):
	inlines = [RuleInline,]

admin.site.register(Challenge, ChallengeAdmin)

from django.contrib import admin

from .models import Challenge, Rule

admin.site.register(Challenge)
admin.site.register(Rule)
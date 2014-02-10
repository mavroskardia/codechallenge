from django.contrib import admin

from .models import Coder, Level


class CoderAdmin(admin.ModelAdmin):
	pass

class LevelAdmin(admin.ModelAdmin):
	list_display_links = ('id',)
	list_display = ('id', 'name', 'starting_xp')
	list_editable = ('name', 'starting_xp')


admin.site.register(Coder, CoderAdmin)
admin.site.register(Level, LevelAdmin)

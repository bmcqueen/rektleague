from django.contrib import admin

from .models import Team
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Player Info', {'fields': ['summoner_name', 'rank']}),
        ('Team Info',   {'fields': ['team', 'role']}),
    ]
    list_display = ('summoner_name', 'team', 'role')


admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)

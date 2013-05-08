from django.contrib import admin
from dance_ave.models import Player, SongStation

class PlayerAdmin(admin.ModelAdmin):
    list_display = (
            'address',
            'completed_stations_count',
            )

class SongStationAdmin(admin.ModelAdmin):
    list_display = (
            'audio_url',
            'select_code',
            )

admin.site.register(Player, PlayerAdmin)
admin.site.register(SongStation, SongStationAdmin)

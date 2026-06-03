from django.contrib import admin
from django.contrib import admin
from .models import Team, Player, Tournament, Match,Lineup, LineupPlayer,MatchEvent
from .models import Standing
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(Standing)
admin.site.register(Lineup)
admin.site.register(LineupPlayer)
admin.site.register(MatchEvent)
# Register your models here.

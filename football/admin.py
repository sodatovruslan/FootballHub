from django.contrib import admin
from django.contrib import admin
from .models import Team, Player, Tournament, Match
from .models import Standing
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(Standing)
# Register your models here.

from django.db import models
from django.db import models
from football.models import Team


class Standing(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE,related_name='stats_standings')

    played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)

    points = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name

from django.db import models
from football.models import Match


class MatchStatistic(models.Model):
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE
    )

    home_shots = models.PositiveIntegerField(default=0)
    away_shots = models.PositiveIntegerField(default=0)

    home_shots_on_target = models.PositiveIntegerField(default=0)
    away_shots_on_target = models.PositiveIntegerField(default=0)

    home_corners = models.PositiveIntegerField(default=0)
    away_corners = models.PositiveIntegerField(default=0)

    home_possession = models.PositiveIntegerField(default=50)
    away_possession = models.PositiveIntegerField(default=50)

    def __str__(self):
        return str(self.match)
# Create your models here.

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
# Create your models here.

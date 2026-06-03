from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='teams/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')

    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    photo = models.ImageField(upload_to='players/', blank=True, null=True)
    overall = models.PositiveIntegerField(default=75)
    pace = models.PositiveIntegerField(default=70)
    shooting = models.PositiveIntegerField(default=70)
    passing = models.PositiveIntegerField(default=70)
    dribbling = models.PositiveIntegerField(default=70)
    defending = models.PositiveIntegerField(default=70)
    physical = models.PositiveIntegerField(default=70)


    def __str__(self):
        return self.full_name
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='home_matches')
    away_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='away_matches')
    date = models.DateTimeField()
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    stream_url = models.URLField(blank=True, null=True)
    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
    


class Standing(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='football_standings')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.team.name} - {self.tournament.name}"
    

class Lineup(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )

    formation = models.CharField(
        max_length=20
    )

    def __str__(self):
        return f"{self.team} - {self.formation}"
    

class LineupPlayer(models.Model):
    lineup = models.ForeignKey(
        Lineup,
        on_delete=models.CASCADE
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )

    position = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.player.full_name
# Create your models here.


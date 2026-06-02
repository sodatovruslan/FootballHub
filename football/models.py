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
    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
# Create your models here.


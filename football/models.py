from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='teams/', blank=True, null=True)
    stadium = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_logo_url(self):
        if self.logo:
            return self.logo.url
        return '/static/images/team-placeholder.png'


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

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return '/static/images/player-placeholder.png'
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
    is_live = models.BooleanField(default=False)
    man_of_the_match = models.ForeignKey(
    Player,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
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

    x_position = models.PositiveIntegerField(default=50, help_text="X position on field (0-100)")
    y_position = models.PositiveIntegerField(default=50, help_text="Y position on field (0-100)")

    def __str__(self):
        return self.player.full_name
    


class MatchEvent(models.Model):
    EVENT_TYPES = [
        ('GOAL', 'Goal'),
        ('ASSIST', 'Assist'),
        ('YELLOW', 'Yellow Card'),
        ('RED', 'Red Card'),
        ('SUB', 'Substitution'),
    ]

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )

    minute = models.PositiveIntegerField()

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    def __str__(self):
        return f"{self.minute}' {self.player.full_name}"


class PlayerMatchRating(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='player_ratings')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_ratings')
    rating = models.DecimalField(max_digits=3, decimal_places=1, help_text="Player rating from 0.0 to 10.0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('match', 'player')

    def __str__(self):
        return f"{self.player.full_name} - {self.rating}"
# Create your models here.


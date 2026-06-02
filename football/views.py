from django.shortcuts import render,get_object_or_404
from .models import Team,Player
from .models import Match

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'football/team_list.html', {'teams': teams})


def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'football/team_detail.html', {'team': team})






def player_list(request):
    players = Player.objects.select_related('team')
    return render(request, 'football/player_list.html', {'players': players})

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'football/player_detail.html', {'player': player})





def match_list(request):
    matches = Match.objects.select_related('home_team', 'away_team', 'tournament')
    return render(request, 'football/match_list.html', {'matches': matches})


def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    return render(request, 'football/match_detail.html', {'match': match})
# Create your views here.

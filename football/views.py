from django.shortcuts import render,get_object_or_404
from .models import Team,Player
from .models import Match
from .models import Standing
from django.urls import reverse_lazy
from django.views import generic

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



# def standings(request):
#     table = Standing.objects.select_related('team', 'tournament').order_by('-points')
#     return render(request, 'football/standings.html', {'table': table})

from django.db.models import Q
from .models import Team, Match


def standings(request):
    teams = Team.objects.all()

    table = []

    for team in teams:
        matches = Match.objects.filter(
            Q(home_team=team) | Q(away_team=team)
        )

        played = matches.count()
        wins = 0
        draws = 0
        losses = 0
        goals_for = 0
        goals_against = 0

        for match in matches:
            if match.home_team == team:
                goals_for += match.home_score
                goals_against += match.away_score

                if match.home_score > match.away_score:
                    wins += 1
                elif match.home_score == match.away_score:
                    draws += 1
                else:
                    losses += 1

            else:
                goals_for += match.away_score
                goals_against += match.home_score

                if match.away_score > match.home_score:
                    wins += 1
                elif match.away_score == match.home_score:
                    draws += 1
                else:
                    losses += 1

        points = wins * 3 + draws

        table.append({
            'team': team,
            'played': played,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'points': points
        })

    table = sorted(table, key=lambda x: x['points'], reverse=True)

    return render(request, 'football/standings.html', {'table': table})



def top_scorers(request):
    players = Player.objects.all()

    scorers = []

    for player in players:
        goals = 0

        matches = Match.objects.filter(
            home_team=player.team
        ) | Match.objects.filter(
            away_team=player.team
        )

      
        scorers.append({
            'player': player,
            'goals': goals
        })

    scorers = sorted(scorers, key=lambda x: x['goals'], reverse=True)

    return render(request, 'football/top_scorers.html', {'scorers': scorers})




class TeamCreateView(generic.CreateView):
    model = Team
    fields = ['name', 'city', 'logo']
    template_name = 'football/team_create.html'
    success_url = reverse_lazy('team_list')
class TeamUpdateView(generic.UpdateView):
    model = Team
    fields = ['name', 'city', 'logo']
    template_name = 'football/team_update.html'
    success_url = reverse_lazy('team_list')
    

class TeamDeleteView(generic.DeleteView):
    model = Team
    template_name = 'football/team_delete.html'
    success_url = reverse_lazy('team_list')
# Create your views here.

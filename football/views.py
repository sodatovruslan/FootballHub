from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Team, Player, Tournament, Match, Standing, Lineup, MatchEvent
from stats.models import MatchStatistic


def home_redirect(request):
    return redirect('team_list')


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
    goals = MatchEvent.objects.filter(
        player=player,
        event_type='GOAL'
    ).count()

    # Get player events grouped by type
    from django.db.models import Count
    events = MatchEvent.objects.filter(
        player=player
    ).values('event_type').annotate(
        count=Count('id')
    )

    context = {
        'player': player,
        'goals': goals,
        'events': events,
    }
    return render(request, 'football/player_detail.html', context)




def standings(request):
    standings_data = Standing.objects.select_related('team', 'tournament').all()
    table = []

    for standing in standings_data:
        goal_difference = standing.goals_for - standing.goals_against
        table.append({
            'team': standing.team,
            'played': standing.played,
            'wins': standing.wins,
            'draws': standing.draws,
            'losses': standing.losses,
            'goals_for': standing.goals_for,
            'goals_against': standing.goals_against,
            'goal_difference': goal_difference,
            'points': standing.points,
            'tournament': standing.tournament
        })

    table = sorted(table, key=lambda x: x['points'], reverse=True)
    return render(request, 'football/standings.html', {'table': table})


def top_scorers(request):
    scorers = (
        MatchEvent.objects
        .filter(event_type='GOAL')
        .values(
            'player__full_name',
            'player__team__name'
        )
        .annotate(goals=Count('id'))
        .order_by('-goals')
    )
    return render(request, 'football/top_scorers.html', {'scorers': scorers})



class TeamCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'football.add_team'
    model = Team
    fields = ['name', 'city', 'logo']
    template_name = 'football/team_create.html'
    success_url = reverse_lazy('team_list')


class TeamUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'football.change_team'
    model = Team
    fields = ['name', 'city', 'logo']
    template_name = 'football/team_update.html'
    success_url = reverse_lazy('team_list')


class TeamDeleteView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'football.delete_team'
    model = Team
    template_name = 'football/team_delete.html'
    success_url = reverse_lazy('team_list')


# Player Views
class PlayerCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'football.add_player'
    model = Player
    fields = ['team', 'full_name', 'age', 'number', 'position', 'photo']
    template_name = 'football/player_create.html'
    success_url = reverse_lazy('player_list')


class PlayerUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'football.change_player'
    model = Player
    fields = ['team', 'full_name', 'age', 'number', 'position', 'photo']
    template_name = 'football/player_update.html'
    success_url = reverse_lazy('player_list')


class PlayerDeleteView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'football.delete_player'
    model = Player
    template_name = 'football/player_delete.html'
    success_url = reverse_lazy('player_list')


# Tournament Views
class TournamentListView(generic.ListView):
    model = Tournament
    template_name = 'football/tournament_list.html'
    context_object_name = 'tournaments'


class TournamentDetailView(generic.DetailView):
    model = Tournament
    template_name = 'football/tournament_detail.html'
    context_object_name = 'tournament'


class TournamentCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'football.add_tournament'
    model = Tournament
    fields = ['name', 'season']
    template_name = 'football/tournament_create.html'
    success_url = reverse_lazy('tournament_list')


class TournamentUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'football.change_tournament'
    model = Tournament
    fields = ['name', 'season']
    template_name = 'football/tournament_update.html'
    success_url = reverse_lazy('tournament_list')


class TournamentDeleteView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'football.delete_tournament'
    model = Tournament
    template_name = 'football/tournament_delete.html'
    success_url = reverse_lazy('tournament_list')


# Match Views
class MatchListView(generic.ListView):
    model = Match
    template_name = 'football/match_list.html'
    context_object_name = 'matches'


class MatchDetailView(generic.DetailView):
    model = Match
    template_name = 'football/match_detail.html'
    context_object_name = 'match'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = self.object
        context['statistic'] = MatchStatistic.objects.filter(match=match).first()
        context['is_started'] = timezone.now() >= match.date
        context['home_lineup'] = Lineup.objects.filter(match=match, team=match.home_team).first()
        context['away_lineup'] = Lineup.objects.filter(match=match, team=match.away_team).first()
        return context


class MatchCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'football.add_match'
    model = Match
    fields = [
        'tournament',
        'home_team',
        'away_team',
        'date',
        'home_score',
        'away_score'
    ]
    template_name = 'football/match_create.html'
    success_url = reverse_lazy('match_list')


class MatchUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'football.change_match'
    model = Match
    fields = [
        'tournament',
        'home_team',
        'away_team',
        'date',
        'home_score',
        'away_score'
    ]
    template_name = 'football/match_update.html'
    success_url = reverse_lazy('match_list')


class MatchDeleteView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'football.delete_match'
    model = Match
    template_name = 'football/match_delete.html'
    success_url = reverse_lazy('match_list')


# MatchEvent Views
class MatchEventListView(generic.ListView):
    model = MatchEvent
    template_name = 'football/match_event_list.html'
    context_object_name = 'match_events'

from django.shortcuts import render,get_object_or_404
from .models import Team


def team_list(request):
    teams = Team.objects.all()
    return render(request, 'football/team_list.html', {'teams': teams})


def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'football/team_detail.html', {'team': team})

# Create your views here.

from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.team_list, name='team_list'),
    path('team/<int:pk>/', views.team_detail, name='team_detail'),
	path('players/', views.player_list, name='player_list'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
	path('matches/', views.match_list, name='match_list'),
    path('match/<int:pk>/', views.match_detail, name='match_detail'),
	path('standings/', views.standings, name='standings'),
	path('top-scorers/', views.top_scorers, name='top_scorers'),
	path('team/create/',views.TeamCreateView.as_view(),name='team_create'),
    path('team/update/<int:pk>/',views.TeamUpdateView.as_view(),name='team_update'),
    path('team/delete/<int:pk>/',views.TeamDeleteView.as_view(),name='team_delete'),
	path('player/create/',views.PlayerCreateView.as_view(),name='player_create'),
    path('player/update/<int:pk>/',views.PlayerUpdateView.as_view(),name='player_update'),
    path('player/delete/<int:pk>/',views.PlayerDeleteView.as_view(),name='player_delete'),
    path('tournaments/',views.TournamentListView.as_view(),name='tournament_list'),
    path('tournament/<int:pk>/',views.TournamentDetailView.as_view(),name='tournament_detail'),
    path('tournament/create/',views.TournamentCreateView.as_view(),   name='tournament_create'),
    path('tournament/update/<int:pk>/',views.TournamentUpdateView.as_view(),name='tournament_update'),
    path('tournament/delete/<int:pk>/',views.TournamentDeleteView.as_view(),name='tournament_delete'),
]
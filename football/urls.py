from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.team_list, name='team_list'),
    path('team/<int:pk>/', views.team_detail, name='team_detail'),
	path('players/', views.player_list, name='player_list'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
	path('matches/', views.match_list, name='match_list'),
     path('match/<int:pk>/', views.match_detail, name='match_detail'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.team_list, name='team_list'),
    path('team/<int:pk>/', views.team_detail, name='team_detail'),
]
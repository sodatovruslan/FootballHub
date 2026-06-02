from django.urls import path
from . import views

urlpatterns = [
    path('', views.standings, name='standings'),
]
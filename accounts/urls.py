from django.urls import path
from . import views

urlpatterns = [
    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'confirm-email/',
        views.confirm_email,
        name='confirm_email'
    ),

    path(
        'forgot-password/',
        views.forgot_password,
        name='forgot_password'
    ),

    path(
        'reset-confirm/',
        views.reset_confirm,
        name='reset_confirm'
    ),

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'profile/update/',
        views.profile_update,
        name='profile_update'
    ),

    path(
        'favorite-team/add/<int:team_id>/',
        views.add_favorite_team,
        name='add_favorite_team'
    ),

    path(
        'favorite-team/remove/',
        views.remove_favorite_team,
        name='remove_favorite_team'
    ),
]
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Match, Standing, MatchEvent
from accounts.models import Profile


@receiver(post_save, sender=Match)
def update_standings(sender, instance, created, **kwargs):
    if not created:
        return
    match=instance
    home=match.home_team
    away = match.away_team
    tournament = match.tournament
    home_st, _ = Standing.objects.get_or_create(team=home,tournament=tournament)
    away_st, _ = Standing.objects.get_or_create(team=away,tournament=tournament)
    home_st.played += 1
    away_st.played += 1
    home_st.goals_for += match.home_score
    home_st.goals_against += match.away_score
    away_st.goals_for += match.away_score
    away_st.goals_against += match.home_score


    if match.home_score > match.away_score:
        home_st.wins += 1
        home_st.points += 3
        away_st.losses += 1

    elif match.home_score < match.away_score:
        away_st.wins += 1
        away_st.points += 3
        home_st.losses += 1

    else:
        home_st.draws += 1
        away_st.draws += 1
        home_st.points += 1
        away_st.points += 1

    home_st.save()
    away_st.save()


@receiver(post_save, sender=Match)
def send_match_notification(sender, instance, created, **kwargs):
    if not created:
        return

    match = instance
    favorite_profiles = Profile.objects.filter(favorite_team__in=[match.home_team, match.away_team])

    for profile in favorite_profiles:
        if profile.favorite_team == match.home_team:
            opponent = match.away_team
            team_name = match.home_team.name
        else:
            opponent = match.home_team
            team_name = match.away_team.name

        subject = f'⚽ Upcoming Match: {match.home_team} vs {match.away_team}'
        message = f'''Hello {profile.user.username}!

Your favorite team {team_name} has a match against {opponent} on {match.date.strftime("%d %B at %H:%M")}.

Don't miss it!

Best regards,
FootballHub Team'''

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[profile.user.email],
            fail_silently=False
        )


@receiver(post_save, sender=MatchEvent)
def send_match_event_notification(sender, instance, created, **kwargs):
    if not created:
        return

    event = instance
    match = event.match
    player = event.player
    team = player.team

    if event.event_type not in ['GOAL', 'ASSIST', 'YELLOW', 'RED']:
        return

    favorite_profiles = Profile.objects.filter(favorite_team=team)

    for profile in favorite_profiles:
        if event.event_type == 'GOAL':
            emoji = '⚽'
            event_text = f'Goal!'
            detail = f'{player.full_name} scored for {team.name} at {event.minute}\''
        elif event.event_type == 'ASSIST':
            emoji = '🎯'
            event_text = f'Assist!'
            detail = f'{player.full_name} provided an assist for {team.name} at {event.minute}\''
        elif event.event_type == 'YELLOW':
            emoji = '🟨'
            event_text = f'Yellow Card'
            detail = f'{player.full_name} received a yellow card at {event.minute}\''
        elif event.event_type == 'RED':
            emoji = '🟥'
            event_text = f'Red Card'
            detail = f'{player.full_name} received a red card at {event.minute}\''

        subject = f'{emoji} {event_text} - {match.home_team} vs {match.away_team}'
        message = f'''Hello {profile.user.username}!

{emoji} {event_text}
{detail}

Match: {match.home_team} vs {match.away_team}

Best regards,
FootballHub Team'''

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[profile.user.email],
            fail_silently=False
        )


@receiver(post_save, sender=Match)
def send_man_of_the_match_notification(sender, instance, **kwargs):
    match = instance
    if not match.man_of_the_match:
        return

    player = match.man_of_the_match
    team = player.team

    favorite_profiles = Profile.objects.filter(favorite_team=team)

    for profile in favorite_profiles:
        subject = f'⭐ Man of the Match - {match.home_team} vs {match.away_team}'
        message = f'''Hello {profile.user.username}!

⭐ Man of the Match

Player {player.full_name} was selected as Man of the Match for {team.name} in the game against {match.home_team if match.away_team == team else match.away_team}.

Best regards,
FootballHub Team'''

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[profile.user.email],
            fail_silently=False
        )
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match, Standing

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
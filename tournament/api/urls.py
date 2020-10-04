from django.urls import path
from tournament.api.views import (api_tournament_view,
                                  api_game_view,
                                  api_player_view, 
                                  api_registration,
                                  get_opted_in_players,
                                  opt_in_tournament,
                                  login_view,
                                  check_session)


app_name = 'tournament'

urlpatterns = [
    path('tournament/<slug>/', api_tournament_view, name='tournament'),
    path('game/<slug>/', api_game_view, name='game'),
    path('player/<int:id>/', api_player_view, name='player'),
    path('register/', api_registration, name='player_register'),
    path('login/', login_view, name='player_login'),
    path('opt_in/', opt_in_tournament, name='opt_in'),
    path('get_opted_in/<tournament_slug>/', get_opted_in_players, name='get_opted_in'),
    path('check_session/<key>', check_session, name='check_session')
]
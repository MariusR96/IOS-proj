import pytz
from datetime import datetime
from rest_framework import viewsets, status
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from tournament.models import Player, Tournament, Game
from tournament.api.serializers import (
    PlayerSerializer,
    GameSerializer,
    TournamentSerializer,
    UserRegistrationSerializer)


@api_view(['GET', ])
def api_tournament_view(request, slug):
    try:
        tournament = Tournament.objects.get(slug=slug)
    except Tournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data)


@api_view(['GET', ])
def api_player_view(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(user)
        return Response(serializer.data)


@api_view(['GET', ])
def api_game_view(request, slug):
    try:
        game = Game.objects.get(slug=slug)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GameSerializer(game)
        return Response(serializer.data)


@api_view(['POST',])
def api_registration(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data_out = {}
            data_out['response'] = 'Successfully registered a new user.'
            data_out['email'] = user.email
            data_out['username'] = user.username
            
        else:
            data_out = serializer.errors

        return Response(data_out)


@api_view(['POST', ])
def login_view(request):
    if request.method == 'POST':
        data_out = {}
        username = request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username,
                            password=password)

        if user is not None:
            login(request, user)                
            data_out['message'] = "Successfully logged in!"
            data_out['key'] = request.session.session_key
            data_out['id'] = user.id
        else:
            data_out['message'] = "User does not exist"
            
    return Response(data_out)


@api_view(['GET',])
def check_session(request, key):
    data_out = {}
    try:
        session = Session.objects.get(pk=key)
        time_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        session_expiry_time = session.expire_date
        
        if session_expiry_time > time_now:
            data_out['is_active'] = True
        else:
            data_out['is_active'] = False

    except Session.DoesNotExist:
        data_out['is_active'] = False
        
    return Response(data_out)


@api_view(['POST', ])
def opt_in_tournament(request):
    data_out = {}
    try:
        player = User.objects.get(pk=request.POST['user_id']).player
        tournament = Tournament.objects.get(slug=request.POST['tournament_slug'])
        tournament.players.add(player)
        data_out['message'] = f"Successfully added the player({player}) to the tournament({tournament.name})."
    
    except Player.DoesNotExist:
        data_out['message'] = "Cannot fint player wit that id."
    
    except Tournament.DoesNotExist:
        data_out['message'] = "Cannot find tournament with that slug."

    return Response(data_out)


@api_view(['GET', ])
def get_opted_in_players(request, tournament_slug):
    data_out={}
    try:
        tournament = Tournament.objects.get(slug=tournament_slug)
        players = tournament.players.all()
        players_in_tournament = [str(player) for player in players]
        data_out['players'] = players_in_tournament

    except Tournament.DoesNotExist:
        data_out['message'] = "Cannot find tournament with that slug."

    return Response(data_out)

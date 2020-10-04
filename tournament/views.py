from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Player, Tournament, Game
from .forms import UserRegistrationForm
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        print(request.session.session_key)
        tournaments = Tournament.objects.all()
        current_user = User.objects.get(pk=request.user.id)
        in_tournaments = []
        out_tournaments = []

        for tournament in tournaments:
            if current_user.player in tournament.players.all():
                in_tournaments.append(tournament)
            else:
                out_tournaments.append(tournament)

        return render(request, 'tournament/index.html', {'title': 'index',
                        'in_tournaments': in_tournaments,
                        'out_tournaments': out_tournaments})
    else: 
        return render(request, 'tournament/index.html', {'title': 'index'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user =  user_form.save()

            messages.success(request, f'Your account has been created!')
            
            return HttpResponseRedirect(reverse('tournament:login'))
    else:
        user_form = UserRegistrationForm()
        
        return render(request, 'tournament/register.html', 
                        {'user_form': user_form})

                        
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f'Welcome, {username} ')
            return HttpResponseRedirect(reverse('tournament:index'))
        else:
            messages.info(request, f'Account does not exist.')

    form = AuthenticationForm()
    return render(request, 'tournament/login.html', {'form': form,
                                'title': 'Login'})


def logout_view(request):
    logout(request)
    return redirect(reverse('tournament:index'))


def check_session(request, key):
    if key in request.session.keys():
        is_active = True
    else:
        is_active = False
    
    return is_active

def tournament_page(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    players = opted_in_players(tournament.slug)
    print(players)
    return render(request, 'tournament/tournament_page.html', {'title': 'Tournament',
                    'tournament': tournament,
                    'opted_in_players': players})


def opt_in_tournaments(request):
    if request.method == 'POST':
        current_user = User.objects.get(pk=request.user.id)
        print(current_user.player)
        for slug in request.POST.getlist('tournament'):
            opt_in(current_user.player, slug)

        return redirect(reverse('tournament:index'))


def opt_in(player, slug):
    tournament = Tournament.objects.get(slug=slug)
    tournament.players.add(player)
    tournament.save()


def opted_in_players(slug):
    tournament = Tournament.objects.get(slug=slug)
    return tournament.players.all()

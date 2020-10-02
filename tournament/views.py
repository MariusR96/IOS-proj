from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Player, Tournament
# Create your views here.

def index(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournament/index.html', {'title': 'index',
                    'tournaments': tournaments})


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


def logout(request):
    logout(request)
    key = request.session.session_key
    return redirect(reverse('tournament:index'))


def check_session(request, key):
    if key in request.session:
        is_active = True
    else:
        is_active = False
    
    return is_active


def opt_in(request, player_id, slug):
    tournament = Tournament.objects.get(slug=slug)
    player = Player.objects.get(pk=player_id)
    tournament.players.add(player)
    tournament.save()


def opted_in_players(request, slug):
    tournament = Tournament.objects.get(slug=slug)
    return tournament.players.all()


def opt_in_tournaments(request):
    print(request.POST) 

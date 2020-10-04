from django.urls import path, include
from . import views



app_name = 'tournament'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.check_session, name='check_session'),
    path('opt_in/', views.opt_in, name='opt_in'),
    path('opt_in_tournaments/', views.opt_in_tournaments, name='opt_in_tournaments'),
    path('tournament_page/<int:tournament_id>', views.tournament_page, name='tournament_page'),
 ]

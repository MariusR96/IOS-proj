from django.urls import path
from . import views


app_name = 'tournament'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.login, name='logout'),
    path('', views.check_session, name='check_session'),
    path('', views.opt_in, name='opt_in'),
    path('', views.opt_in_tournaments, name='opt_in_tournaments'),
]
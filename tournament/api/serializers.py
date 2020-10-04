from rest_framework import serializers
from tournament.models import User, Game, Tournament, Player
from django.contrib.auth.hashers import make_password

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        #fields = ('id', 'username', 'email')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'slug', 'thumbnail', 'release_date', 'tournament')


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'slug', 'points_addition', 'start_date', 'expiry_date', 'players')


class UserRegistrationSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ['username', 'email', 'password' ]
        extra_kwargs = {
            'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            password=make_password(self.validated_data['password']),

        )

        user.save()
        return user
    
import datetime 
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class Player(models.Model):
    user = models.OneToOneField(User,
         on_delete=models.CASCADE)
    
    points_field = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.points_field} points'

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:     
        Player.objects.create(user=instance)
    instance.player.save()


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=20)
    points_addition = models.IntegerField()
    start_date = models.DateTimeField('Start Date')
    expiry_date = models.DateTimeField('Expiry Date')
    players = models.ManyToManyField('Player')

    def __str__(self):
        return f'{self.name}'

class Game(models.Model):
    name = name = models.CharField(max_length=50)
    slug = models.CharField(max_length=20)
    thumbnail = models.CharField(max_length=50)
    release_date = models.DateTimeField('Release Date')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
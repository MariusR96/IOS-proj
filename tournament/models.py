import datetime 
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
#from rest_framework.authtoken.models import Token

class Player(models.Model):
    user = models.OneToOneField(User,
         on_delete=models.CASCADE)
    
    points_field = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:     
        Player.objects.create(user=instance)
    instance.player.save()


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    points_addition = models.IntegerField()
    start_date = models.DateTimeField('Start Date')
    expiry_date = models.DateTimeField('Expiry Date')
    players = models.ManyToManyField('Player', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tournament, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Game(models.Model):
    name = name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    thumbnail = models.CharField(max_length=50)
    release_date = models.DateTimeField('Release Date')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
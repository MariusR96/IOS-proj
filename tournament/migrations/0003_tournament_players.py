# Generated by Django 3.0.2 on 2020-10-02 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20201002_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='players',
            field=models.ManyToManyField(to='tournament.Player'),
        ),
    ]

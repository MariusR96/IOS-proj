# Generated by Django 3.0.2 on 2020-10-02 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='player',
            new_name='user',
        ),
    ]

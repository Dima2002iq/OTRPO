# Generated by Django 4.2.6 on 2023-12-01 08:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0003_event_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='pokemon_pc',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='pokemon_player',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='pokemon_winner',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

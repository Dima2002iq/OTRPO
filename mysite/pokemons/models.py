from django.db import models


class Event(models.Model):
    description = models.CharField(max_length=200)
    pokemon_player = models.IntegerField(default=0)
    pokemon_pc = models.IntegerField(default=0)
    pokemon_winner = models.IntegerField(default=0)
    rounds = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description

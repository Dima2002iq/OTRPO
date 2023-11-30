from django.db import models


class Event(models.Model):
    description = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description

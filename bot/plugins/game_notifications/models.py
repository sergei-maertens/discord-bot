from django.db import models


class GameNotification(models.Model):
    game_name = models.CharField('name', max_length=255)
    user = models.CharField('user', max_length=255)

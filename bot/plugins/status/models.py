from django.db import models


class GameStatus(models.Model):

    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status

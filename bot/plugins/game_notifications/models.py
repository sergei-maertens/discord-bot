from django.db import models


class GameNotification(models.Model):
    game_name = models.CharField('name', max_length=255)
    user = models.CharField('user', max_length=255)

    last_notification = models.DateTimeField(auto_now=True, null=True)
    muted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('game_name', 'user')

    def __str__(self):
        return 'Subscription for {game} by member {id}'.format(game=self.game_name, id=self.user)

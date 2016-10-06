from django.db import models
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _


class LoggedMessage(models.Model):

    discord_id = models.CharField(max_length=50, unique=True)

    member = models.ForeignKey('users.Member', related_name='messages_authored', on_delete=models.PROTECT)
    member_username = models.CharField(max_length=255)  # this can change, only the member.discord_id is a constant

    channel = models.ForeignKey('channels.Channel', on_delete=models.PROTECT)

    content = models.TextField()
    num_lines = models.PositiveSmallIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_timestamp = models.DateTimeField(null=True, blank=True)

    mentions = models.ManyToManyField('users.Member', related_name='messages_mentioned_in', blank=True)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ['-timestamp']

    def __str__(self):
        return self.discord_id


class GameSessionQuerySet(models.QuerySet):

    def get_game_durations(self):
        return self.filter(duration__isnull=False).values('game__name').annotate(
            time=Sum('duration'),
            num_players=Count('member', distinct=True)
        ).filter(num_players__gt=1).order_by('-time')


class GameSession(models.Model):
    member = models.ForeignKey('users.Member', on_delete=models.PROTECT)
    game = models.ForeignKey('games.Game')
    start = models.DateTimeField(_('start'))
    stop = models.DateTimeField(_('stop'), null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    objects = GameSessionQuerySet.as_manager()

    class Meta:
        verbose_name = _('game session')
        verbose_name_plural = _('game sessions')

    def __str__(self):
        return self.game.name


class Download(models.Model):
    title = models.CharField(_('title'), max_length=255)
    file = models.FileField(upload_to='downloads/%Y/%m/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('download')
        verbose_name_plural = _('downloads')

    def __str__(self):
        return self.title

from typing import Union

import discord
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from bot.games.models import Game
from bot.users.models import Member


class LoggedMessage(models.Model):

    discord_id = models.BigIntegerField(unique=True)
    server = models.BigIntegerField(_("server"))

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

    def get_game_durations(self, member_id: str = None) -> models.QuerySet:
        base = self.filter(duration__isnull=False).values('game__name')
        annotations, extra_filters = dict(time=Sum('duration')), {}

        if not member_id:
            annotations['num_players'] = Count('member', distinct=True)
            extra_filters['num_players__gt'] = 1
        else:
            base = base.filter(member__discord_id=member_id)

        return (
            base
            .annotate(**annotations)
            .filter(**extra_filters)
            .order_by('-time')
        )

    def start(self, game: discord.Game, member: Member, server: str) -> models.Model:
        game = Game.objects.get_by_name(game.name)
        return self.create(
            server=server,
            member=member,
            game=game,
            start=timezone.now()
        )

    def last_session_for_member(self, member: Member, server: str) -> Union[None, models.Model]:
        try:
            last_session = (
                self
                .filter(member=member, server=server)
                .latest('start')
            )
        except self.model.DoesNotExist:
            return None
        return last_session


class GameSession(models.Model):
    member = models.ForeignKey('users.Member', on_delete=models.PROTECT)
    server = models.BigIntegerField(_("server"))
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
    start = models.DateTimeField(_('start'))
    stop = models.DateTimeField(_('stop'), null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    objects = GameSessionQuerySet.as_manager()

    class Meta:
        verbose_name = _('game session')
        verbose_name_plural = _('game sessions')

    def __str__(self):
        return self.game.name

    def save(self, *args, **kwargs):
        if self.stop and not self.duration:
            self.duration = self.stop - self.start
        super().save(*args, **kwargs)

    def stop_session(self):
        self.stop = timezone.now()
        self.save()


class Download(models.Model):
    title = models.CharField(_('title'), max_length=255)
    file = models.FileField(upload_to='downloads/%Y/%m/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('download')
        verbose_name_plural = _('downloads')

    def __str__(self):
        return self.title

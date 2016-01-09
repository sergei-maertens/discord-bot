import logging
import re

from discord.enums import Status
from django.conf import settings

from bot.plugins.base import BasePlugin

from .models import GameNotification


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True
    subscribe_pattern = re.compile(r'!subscribe (?P<game>.+)', re.IGNORECASE)
    unsubscribe_pattern = re.compile(r'!unsubscribe (?P<game>.+)', re.IGNORECASE)

    help = (
        '`!subscribe <game>` sets up notifications for that game\n'
        '`!unsubscribe <game>` deletes your subscription\n'
        '`!unsubscribe !all` deletes all your subscriptions\n'
        'Commands are case-insensitive'
    )

    def _member_active(self, member):
        statuses = [Status.online, Status.idle]
        gaming = member.game and settings.DEBUG is False
        return member.status in statuses and not member.is_afk and not gaming

    def on_member_update(self, before, after):
        if not after.game:
            return

        member = after
        game = member.game.name
        subscribers = GameNotification.objects.filter(game_name__iexact=game)
        if settings.DEBUG:
            subscribers = subscribers.filter(user=member.id)
        else:
            subscribers = subscribers.exclude(user=member.id)
        if not subscribers.exists():
            return

        ids = subscribers.values_list('user', flat=True)
        members = [m for m in member.server.members if m.id in ids and self._member_active(m)]
        if not members:
            return

        msg = '{name} started playing {game}'.format(name=member.name, game=game)
        for member in members:
            logger.info('Notifying %s for %s', member.name, game)
            yield from self.client.send_message(member, msg)

    def on_message(self, message):
        user = message.author.id

        match = re.match(self.subscribe_pattern, message.content)
        if match:
            game = match.group('game').strip()
            notification, created = GameNotification.objects.get_or_create(game_name=game.lower(), user=user)
            msg = 'Subscribed you to {game}' if created else 'You were already subscribed to {game}'
            yield from self.client.send_message(message.channel, msg.format(game=game))
            return

        match = re.match(self.unsubscribe_pattern, message.content)
        if match:
            game = match.group('game').strip()
            if game.lower() == '!all':
                deleted, _ = GameNotification.objects.filter(user=user).delete()
                yield from self.client.send_message(
                    message.channel,
                    'Unsubscribed you from {num} games'.format(num=deleted)
                )
                return

            deleted, _ = GameNotification.objects.filter(user=user, game_name__iexact=game).delete()
            if deleted:
                yield from self.client.send_message(
                    message.channel,
                    'Unsubscribed you from {game} games'.format(game=game)
                )
            return

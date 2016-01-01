import logging
import re

from bot.plugins.base import BasePlugin

from .models import GameNotification


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    subscribe_pattern = re.compile(r'!subscribe (?P<game>.+)', re.IGNORECASE)
    unsubscribe_pattern = re.compile(r'!unsubscribe (?P<game>.+)', re.IGNORECASE)
    channel = 'general'

    help = (
        '`!subscribe <game>` sets up notifications for that game\n'
        '`!unsubscribe <game>` deletes your subscription\n'
        '`!unsubscribe !all` deletes all your subscriptions\n'
        'Commands are case-insensitive'
    )

    def _member_active(self, member):
        return member.status in ['online', 'idle'] and not member.is_afk and not member.game

    def on_status(self, member, old_game, old_status):
        if member.game:
            game = member.game.name
            subscribers = GameNotification.objects.filter(game_name__iexact=game).exclude(user=member.id)
            if not subscribers.exists():
                return

            ids = subscribers.values_list('user', flat=True)
            members = [m for m in member.server.members if m.id in ids and self._member_active(m)]
            if not members:
                return

            mentions = ', '.join([m.mention() for m in members])
            msg = '{mentions}: {name} started playing {game}'.format(mentions=mentions, name=member.name, game=game)
            channel = next((c for c in member.server.channels if c.name == self.channel), None)
            self.client.send_message(channel, msg)

    def on_message(self, message):
        user = message.author.id

        match = re.match(self.subscribe_pattern, message.content)
        if match:
            game = match.group('game').strip()
            notification, created = GameNotification.objects.get_or_create(game_name=game.lower(), user=user)
            msg = 'Subscribed you to {game}' if created else 'You were already subscribed to {game}'
            self.client.send_message(message.channel, msg.format(game=game))
            return

        match = re.match(self.unsubscribe_pattern, message.content)
        if match:
            game = match.group('game').strip()
            if game.lower() == '!all':
                deleted, _ = GameNotification.objects.filter(user=user).delete()
                self.client.send_message(message.channel, 'Unsubscribed you from {num} games'.format(num=deleted))
                return

            deleted, _ = GameNotification.objects.filter(user=user, game_name__iexact=game).delete()
            if deleted:
                self.client.send_message(message.channel, 'Unsubscribed you from {game} games'.format(game=game))
            return

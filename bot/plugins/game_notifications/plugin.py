import logging
import re

from bot.plugins.base import BasePlugin

from .models import GameNotification


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    subscribe_pattern = re.compile(r'!subscribe (?P<game>.+)', re.IGNORECASE)
    unsubscribe_pattern = re.compile(r'!unsubscribe (?P<game>.+)', re.IGNORECASE)

    def on_status(self, member, old_game, old_status):
        if member.game:
            import bpdb; bpdb.set_trace()

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

            deleted = GameNotification.objects.filter(user=user, game_name__iexact=game)
            if deleted:
                self.client.send_message(message.channel, 'Unsubscribed you from {game} games'.format(game=game))
            return

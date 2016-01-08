import logging
import re

from discord.enums import Status

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command

from .models import GameNotification


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    # TODO: refactor into the command API
    help = (
        '`!subscribe <game>` sets up notifications for that game\n'
        '`!unsubscribe <game>` deletes your subscription\n'
        '`!unsubscribe_all` deletes all your subscriptions\n'
        'Commands are case-insensitive'
    )

    def _member_active(self, member):
        statuses = [Status.online, Status.idle]
        return member.status in statuses and not member.is_afk and not member.game

    def on_member_update(self, before, after):
        if after.game and after.game != before.game:
            member = after
            game = member.game.name
            subscribers = GameNotification.objects.filter(game_name__iexact=game).exclude(user=member.id)
            if not subscribers.exists():
                return

            ids = subscribers.values_list('user', flat=True)
            members = [m for m in member.server.members if m.id in ids and self._member_active(m)]
            if not members:
                return

            msg = '{name} started playing {game}'.format(name=member.name, game=game)
            for member in members:
                yield from self.client.send_message(member, msg)
                logger.info('Notified %s for %s', member.name, game)

    @command(pattern=re.compile(r'(?P<game>.+)', re.IGNORECASE))
    def subscribe(self, command):
        user = command.message.author.id
        game = command.args.game
        notification, created = GameNotification.objects.get_or_create(game_name=game.lower(), user=user)
        msg = 'Subscribed you to {game}' if created else 'You were already subscribed to {game}'
        yield from command.reply(msg.format(game=game))

    @command(pattern=re.compile(r'(?P<game>.+)', re.IGNORECASE))
    def unsubscribe(self, command):
        user = command.message.author.id
        game = command.args.game
        deleted, _ = GameNotification.objects.filter(user=user, game_name__iexact=game).delete()
        if deleted:
            yield from command.reply('Unsubscribed you from {game}'.format(game=game))

    @command()
    def unsubscribe_all(self, command):
        user = command.message.author.id
        deleted, _ = GameNotification.objects.filter(user=user).delete()
        yield from command.reply('Unsubscribed you from {num} games'.format(num=deleted))

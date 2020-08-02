import logging

from discord.enums import Status
from discord import Game
from django.conf import settings

from bot.plugins.base import BasePlugin
from bot.plugins.commands import PREFIX, Command

from .models import CommandAction

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    def _member_active(self, member):
        statuses = [Status.online, Status.idle]
        gaming = settings.DEBUG is False and any(
            (isinstance(activity, Game) for activity in member.activities)
        )
        return member.status in statuses and not member.is_afk and not gaming

    async def on_message(self, message):
        await super().on_message(message)

        if not message.content.startswith(PREFIX):
            return

        command = Command(None, for_message=message)
        command.client = self.client

        cmd = message.content[len(PREFIX):]
        # try to match a command and fetch an action
        action = CommandAction.objects.filter(command__command__iexact=cmd).order_by('?').first()
        if action:
            await command.trigger_typing()
            await command.reply(action.action)

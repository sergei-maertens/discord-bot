import logging

from bot.channels.models import Channel
from bot.plugins.base import BasePlugin
from bot.users.models import Member

from .models import LoggedMessage


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    def on_message(self, message):
        """
        Log the message in the db
        """
        super().on_message(message)

        member = Member.objects.from_message(message)
        channel = Channel.objects.from_message(message)

        n_lines = len(message.content.splitlines())

        logged_message = LoggedMessage.objects.create(
            discord_id=message.id, member=member,
            member_username=message.author.name,
            channel=channel, content=message.content,
            num_lines=n_lines
        )
        if message.mentions:
            logged_message.mentions = Member.objects.from_mentions(message.mentions)

    def on_message_edit(self, before, after):
        import bpdb; bpdb.set_trace()

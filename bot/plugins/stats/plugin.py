import logging

from django.db.models import Count
from django.utils.timezone import make_aware, utc

from tabulate import tabulate

from bot.channels.models import Channel
from bot.plugins.base import BasePlugin
from bot.plugins.commands import command
from bot.users.models import Member

from .models import LoggedMessage


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    def on_message(self, message):
        """
        Log the message in the db
        """
        yield from super().on_message(message)

        if message.channel.is_private:
            return

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
        yield from super().on_message_edit(before, after)

        logged_message = LoggedMessage.objects.filter(discord_id=before.id).first()
        if not logged_message:
            return

        logged_message.edited_timestamp = make_aware(after.edited_timestamp, utc)
        logged_message.content = after.content
        logged_message.num_lines = len(after.content.splitlines())
        logged_message.save()

    # TODO: track status changes -> log how long anyone plays a game

    @command(help='Show the top 10 posters')
    def stat_messages(self, command):
        yield from command.send_typing()
        queryset = Member.objects.annotate(num_messages=Count('messages_authored'))
        top_10 = queryset.order_by('-num_messages')[:10]
        data = [(member.name or str(member), member.num_messages) for member in top_10]
        output = tabulate(data, headers=('User', 'messages'))
        yield from command.reply("```\n{}\n```".format(output))

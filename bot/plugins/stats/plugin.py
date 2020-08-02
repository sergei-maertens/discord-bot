import logging
import re

from discord.channel import TextChannel
from discord.enums import Status
from django.db.models import Count, Q
from django.utils.timesince import timesince
from django.utils.timezone import make_aware, now, utc
from import_export.admin import DEFAULT_FORMATS
from tabulate import tabulate

from bot.channels.models import Channel
from bot.plugins.base import BasePlugin
from bot.plugins.commands import command
from bot.users.models import Member

from .models import LoggedMessage

logger = logging.getLogger(__name__)


EXPORT_FORMATS = {f().get_title(): f for f in DEFAULT_FORMATS if f().can_export()}


class Plugin(BasePlugin):

    has_blocking_io = True

    async def on_message(self, message):
        """
        Log the message in the db
        """
        await super().on_message(message)

        if not isinstance(message.channel, TextChannel):
            return

        member = Member.objects.from_message(message)
        channel = Channel.objects.from_message(message)

        n_lines = len(message.content.splitlines())

        logged_message = LoggedMessage.objects.create(
            server=message.guild.id,
            discord_id=message.id, member=member,
            member_username=message.author.name,
            channel=channel, content=message.content,
            num_lines=n_lines
        )
        if message.mentions:
            logged_message.mentions.set(
                Member.objects.from_mentions(message.mentions)
            )

    async def on_message_edit(self, before, after):
        await super().on_message_edit(before, after)

        logged_message = LoggedMessage.objects.filter(discord_id=before.id).first()
        if not logged_message:
            return

        if after is not None:
            if after.edited_timestamp:
                logged_message.edited_timestamp = make_aware(after.edited_timestamp, utc)
            logged_message.content = after.content
            logged_message.num_lines = len(after.content.splitlines())
            logged_message.save()

    @command(help='Show the top 10 posters')
    async def stat_messages(self, command):
        await command.trigger_typing()
        server_id = command.message.guild.id
        queryset = (
            Member.objects
            .exclude(is_bot=True)
            .annotate(num_messages=Count(
                'messages_authored',
                filter=Q(messages_authored__server=server_id)
            ))
        )
        top_10 = queryset.order_by('-num_messages')[:10]
        data = [(member.name or str(member), member.num_messages) for member in top_10]
        output = tabulate(data, headers=('User', 'Messages'))
        await command.reply("```\n{}\n```".format(output))

    @command(pattern=re.compile(r'(?P<name>.*)', re.IGNORECASE))
    async def seen(self, command):
        if command.message.mentions:
            if len(command.message.mentions) > 1:
                await command.reply('Supply one user at a time')
                return
            d_member = command.message.mentions[0]
            member = Member.objects.filter(discord_id=d_member.id).first()
            username = d_member.name
        else:
            username = command.args.name
            member = Member.objects.filter(name__iexact=username).first()
            all_members = command.message.channel.guild.members
            d_member = next((m for m in all_members if m.name.lower() == username.lower()), None)

        if d_member and d_member.status == Status.online:
            await command.reply('{} is currently online'.format(d_member.name))
            if member:
                member.last_seen = now()
                member.save()
            return

        if not member or not member.last_seen:
            await command.reply('Haven\'t seen {} (yet)'.format(username))
            return

        if member:
            last_message = member.messages_authored.latest('timestamp')
            reply1 = "{name} was last seen: {last_seen} ago".format(
                name=username,
                last_seen=timesince(member.last_seen)
            )
            reply2 = "The last message was: ```{message}```".format(message=last_message.content)
            await command.reply("{}\n{}".format(reply1, reply2))

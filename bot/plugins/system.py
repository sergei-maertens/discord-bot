import asyncio
import datetime
import logging
import os
import platform

import psutil
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince

from bot.plugins.base import BasePlugin
from bot.users.models import Member


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    command_map = {
        '!restart': 'restart',
        '!sysinfo': 'sysinfo',
    }

    def on_message(self, message):
        cmd = message.content.lower()
        if cmd in self.command_map:
            logger.debug('Received command `{}`'.format(cmd))
            handler = getattr(self, self.command_map[cmd])
            yield from handler(message)

    @asyncio.coroutine
    def restart(self, message):
        """
        Restarts the bot.

        Check that the person sending the command has permission to restart the bot.
        We rely on ``supervisord`` here - if the process dies, supervisord will
        bring it back up.

        FIXME: https://docs.python.org/3/library/asyncio-dev.html#pending-task-destroyed
        """
        author_id = message.author.id
        qs = Member.objects.filter(discord_id=author_id, can_admin_bot=True)
        if author_id == self.options['owner_id'] or qs.exists():
            logger.info('Restart issued by %s, with ID %s', message.author.name, author_id)
            yield from self.client.send_typing(message.channel)
            yield from self.client.send_message(message.channel, 'Restarting...')
            yield from asyncio.sleep(1)
            raise KeyboardInterrupt
        else:
            yield from self.client.send_message(message.channel, 'Nope, denied.')

    @asyncio.coroutine
    def sysinfo(self, message):
        process = psutil.Process(os.getpid())
        mem_usage = process.memory_info().rss
        created = datetime.datetime.fromtimestamp(int(process.create_time()))
        msg = (
            "Uptime: {uptime}\n"
            "Memory usage: {mem}\n"
            "OS: {system}, {release}\n"
        ).format(
            mem=filesizeformat(mem_usage),
            uptime=timesince(created),
            system=platform.system(),
            release=platform.release(),
        )
        yield from self.client.send_message(message.channel, msg)

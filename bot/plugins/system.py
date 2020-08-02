import datetime
import logging
import os
import platform
import re
from io import StringIO

import psutil
from django.conf import settings
from django.core.management import call_command
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command
from bot.users.decorators import bot_admin_required

logger = logging.getLogger(__name__)


RE_CHECKOUT = re.compile(r'(?P<branch>.+)$', re.IGNORECASE)


class Plugin(BasePlugin):

    has_blocking_io = True

    @command()
    @bot_admin_required
    async def restart(self, command):
        """
        Restarts the bot.

        Check that the person sending the command has permission to restart the bot.
        We rely on ``supervisord`` here - if the process dies, supervisord will
        bring it back up.

        FIXME: https://docs.python.org/3/library/asyncio-dev.html#pending-task-destroyed
        """
        author_id = command.message.author.id
        logger.info('Restart issued by %s, with ID %d', command.message.author.name, author_id)
        await command.trigger_typing()
        await command.reply('Restarting...')
        raise KeyboardInterrupt

    @command()
    async def sysinfo(self, command):
        """
        Shows system/bot information
        """
        process = psutil.Process(os.getpid())
        mem_usage = process.memory_info().rss
        created = datetime.datetime.fromtimestamp(int(process.create_time()))

        msg = (
            f"Uptime: `{timesince(created)}`\n"
            f"Memory usage: `{filesizeformat(mem_usage)}`\n"
            f"OS: `{platform.system()}, {platform.release()}`\n"
            f"{settings.SITE_URL}, \n{settings.GITHUB_URL}\n"
        )
        await command.reply(msg)

    @command()
    @bot_admin_required
    async def migrate(self, command):
        """
        Migrates the database forward
        """
        out = StringIO()
        call_command('migrate', interactive=False, no_color=True, stdout=out)
        out.seek(0)
        await command.reply(out.read())

    @command(help="Shows your discord user id")
    async def discord_id(self, command):
        member = command.message.author
        await command.reply('{0.mention}: {0.id}'.format(member))

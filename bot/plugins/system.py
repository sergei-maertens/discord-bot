import asyncio
import datetime
import logging
import os
import platform
import re

import psutil
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince
from git import Repo

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command
from bot.users.models import Member


logger = logging.getLogger(__name__)


RE_CHECKOUT = re.compile(r'(?P<branch>.+)$', re.IGNORECASE)


class Plugin(BasePlugin):

    has_blocking_io = True

    def is_admin(self, message):
        author_id = message.author.id
        qs = Member.objects.filter(discord_id=author_id, can_admin_bot=True)
        return author_id == self.options['owner_id'] or qs.exists()

    @command()
    def restart(self, command):
        """
        Restarts the bot.

        Check that the person sending the command has permission to restart the bot.
        We rely on ``supervisord`` here - if the process dies, supervisord will
        bring it back up.

        FIXME: https://docs.python.org/3/library/asyncio-dev.html#pending-task-destroyed
        """
        author_id = command.message.author.id
        if self.is_admin(command.message):
            logger.info('Restart issued by %s, with ID %s', command.message.author.name, author_id)
            yield from command.send_typing()
            yield from command.reply('Restarting...')
            raise KeyboardInterrupt
        else:
            yield from command.reply('Nope, denied.')

    @command()
    def sysinfo(self, command):
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
        yield from command.reply(msg)

    @command('git checkout', pattern=RE_CHECKOUT)
    def git_checkout(self, command):
        if not self.is_admin(command.message):
            yield from command.reply('Nope, denied.')
            return

        repo = Repo(settings.PROJECT_ROOT)
        branch = command.args.branch
        try:
            head = getattr(repo.heads, branch)
        except AttributeError:
            yield from command.reply('Branch `%s` does not exist' % branch)
        else:
            head.checkout()
            yield from command.reply('Checked out `%s`' % branch)
        return

    @command('git pull')
    def get_pull(self, command):
        if not self.is_admin(command.message):
            yield from command.reply('Nope, denied.')
            return

        repo = Repo(settings.PROJECT_ROOT)
        repo.remotes.origin.pull()
        yield from command.reply('Pulled the latest commits')

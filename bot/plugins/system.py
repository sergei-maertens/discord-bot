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
from git import Repo

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command
from bot.users.decorators import bot_admin_required


logger = logging.getLogger(__name__)


RE_CHECKOUT = re.compile(r'(?P<branch>.+)$', re.IGNORECASE)


class Plugin(BasePlugin):

    has_blocking_io = True

    @command()
    @bot_admin_required
    def restart(self, command):
        """
        Restarts the bot.

        Check that the person sending the command has permission to restart the bot.
        We rely on ``supervisord`` here - if the process dies, supervisord will
        bring it back up.

        FIXME: https://docs.python.org/3/library/asyncio-dev.html#pending-task-destroyed
        """
        author_id = command.message.author.id
        logger.info('Restart issued by %s, with ID %s', command.message.author.name, author_id)
        yield from command.send_typing()
        yield from command.reply('Restarting...')
        raise KeyboardInterrupt

    @command()
    def sysinfo(self, command):
        """
        Shows system/bot information
        """
        process = psutil.Process(os.getpid())
        mem_usage = process.memory_info().rss
        created = datetime.datetime.fromtimestamp(int(process.create_time()))

        repo = Repo(settings.PROJECT_ROOT)

        msg = (
            "Uptime: `{uptime}`\n"
            "Memory usage: `{mem}`\n"
            "OS: `{system}, {release}`\n"
            "Current branch: `{branch}`, `{commit}`, \n`{message}`\n"
            "{website}, \n{github}\n"
        ).format(
            mem=filesizeformat(mem_usage),
            uptime=timesince(created),
            system=platform.system(),
            release=platform.release(),
            branch=repo.active_branch.name,
            commit=repo.active_branch.commit.hexsha,
            message=repo.active_branch.commit.message,
            website=settings.SITE_URL,
            github=settings.GITHUB_URL
        )
        yield from command.reply(msg)

    @command(pattern=RE_CHECKOUT)
    @bot_admin_required
    def git_checkout(self, command):
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

    @command()
    @bot_admin_required
    def git_pull(self, command):
        repo = Repo(settings.PROJECT_ROOT)
        repo.remotes.origin.pull()
        yield from command.reply('Pulled the latest commits')

    @command()
    @bot_admin_required
    def migrate(self, command):
        """
        Migrates the database forward
        """
        out = StringIO()
        call_command('migrate', interactive=False, no_color=True, stdout=out)
        out.seek(0)
        yield from command.reply(out.read())

    @command()
    @bot_admin_required
    def update_self(self, command):
        """
        Shortcut to update current branch
        """
        yield from command.reply('Starting full self update...')
        yield from self.git_pull(command)
        yield from self.migrate(command)
        yield from self.sysinfo(command)
        yield from self.restart(command)

    @command(help="Shows your discord user id")
    def discord_id(self, command):
        member = command.message.author
        yield from command.reply('{0.mention}: {0.id}'.format(member))

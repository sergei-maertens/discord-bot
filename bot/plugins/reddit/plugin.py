import logging
import re
from datetime import timedelta

from discord.enums import Status
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command

from .models import RedditCommand


logger = logging.getLogger(__name__)

COOLDOWN = 5*60  # 5 minutes


class Plugin(BasePlugin):

    has_blocking_io = True

    @command(pattern=re.compile(r'!?(?P<cmd>.*): (?P<subreddit>.*)', re.IGNORECASE))
    def add_subreddit(self, command):
        cmd, subreddit = command.args.cmd, command.args.subreddit
        reddit_cmd, created = RedditCommand.objects.get_or_create(
            command=cmd, defaults={'subreddit': subreddit}
        )
        tpl = 'Added %r' if created else 'Command already exists: %r'
        yield from command.reply(tpl % reddit_cmd)

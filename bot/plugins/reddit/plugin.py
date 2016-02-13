import logging
import random
import re

import praw
from django.db.models import F

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command, Command, PREFIX

from .models import RedditCommand


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reddit_bot = praw.Reddit(user_agent=self.options['useragent'])

    @command(
        pattern=re.compile(r'!?(?P<cmd>.*): (?P<subreddit>.*)', re.IGNORECASE),
        help='Configure a command to show a subreddit submission'
    )
    def add_subreddit(self, command):
        cmd, subreddit = command.args.cmd, command.args.subreddit
        reddit_cmd, created = RedditCommand.objects.get_or_create(
            command=cmd, defaults={'subreddit': subreddit}
        )
        tpl = 'Added %r' if created else 'Command already exists: %r'
        yield from command.reply(tpl % reddit_cmd)

    @command(help='Lists the command to fetch submissions from a subreddit')
    def list_subreddits(self, command):
        i = 0
        for reddit_cmd in RedditCommand.objects.all():
            i += 1
            yield from command.reply('{i}. {cmd} ({used}x used)'.format(
                i=i, cmd=reddit_cmd, used=reddit_cmd.times_used)
            )

    def on_message(self, message):
        yield from super().on_message(message)

        if not message.content.startswith(PREFIX):
            return

        command = Command(None, for_message=message)
        command.client = self.client

        cmd = message.content[len(PREFIX):]
        try:
            reddit_cmd = RedditCommand.objects.get(command=cmd)
            reddit_cmd.times_used = F('times_used') + 1
            reddit_cmd.save()
        except RedditCommand.DoesNotExist:
            return

        yield from command.send_typing()
        subreddit = self.reddit_bot.get_subreddit(reddit_cmd.subreddit)
        logger.debug('Fetched subreddit %s', reddit_cmd.subreddit)
        submissions = [s for s in subreddit.get_hot(limit=50)]
        submission = random.choice(submissions)
        logger.debug('Picked a submission')
        yield from command.reply(submission.url)
        logger.debug('Sent message')

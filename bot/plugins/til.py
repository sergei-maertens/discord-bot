import logging
import random

import praw

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reddit_bot = praw.Reddit(user_agent=self.options['useragent'])

    @command()
    def til(self, command):
        """
        Shows a random submission from r/todayilearned
        """
        yield from command.send_typing()
        subreddit = self.reddit_bot.get_subreddit(self.options['subreddit'])
        logger.debug('Fetched subreddit')
        submissions = [s for s in subreddit.get_hot(limit=50) if s.url]
        submission = random.choice(submissions)
        logger.debug('Picked a submission')
        yield from command.reply('{title}\n{url}'.format(url=submission.url, title=submission.title))

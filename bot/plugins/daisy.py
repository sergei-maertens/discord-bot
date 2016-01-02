import logging
import random

import praw

from bot.plugins.base import BasePlugin


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reddit_bot = praw.Reddit(user_agent=self.options['useragent'])

    def on_message(self, message):
        if message.content == '!dr':
            yield from self.client.send_typing(message.channel)
            subreddit = self.reddit_bot.get_subreddit(self.options['subreddit'])
            logger.debug('Fetched subreddit')
            submissions = [s for s in subreddit.get_hot(limit=50) if 'imgur' in s.url]
            submission = random.choice(submissions)
            logger.debug('Picked a submission')
            yield from self.client.send_message(message.channel, submission.url)
            logger.debug('Sent message')

import logging
import random

import praw

from bot.plugins.base import BasePlugin


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reddit_bot = praw.Reddit(user_agent=self.options['useragent'])

    def on_message(self, message):
        if message.content.startswith('!daisy'):
            subreddit = self.reddit_bot.get_subreddit(self.options['subreddit'])
            submissions = [s for s in subreddit.get_hot(limit=50) if not s.selftext and 'imgur' in s.url]
            submission = random.choice(submissions)
            self.client.send_message(message.channel, submission.url)

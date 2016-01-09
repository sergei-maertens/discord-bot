import logging

from bot.plugins.base import BasePlugin


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    def on_message(self, message):
        channel = getattr(message.channel, 'name', None)
        if channel != 'developer':
            return

        if message.content.startswith('!pm'):
            yield from self.client.send_message(message.author, 'HAI')

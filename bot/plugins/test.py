import logging

from bot.plugins.base import BasePlugin


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    def on_message(self, message):
        if message.channel.name != 'developer':
            return

        if message.content.startswith('!test'):
            yield from self.client.send_message(message.channel, 'Yeah yeah it\'s fine')

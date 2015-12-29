import logging

from .base import BasePlugin


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    def on_message(self, message):
        if message.content.startswith('!daisy'):
            self.client.send_message(message.channel, '<3')

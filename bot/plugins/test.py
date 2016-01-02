import asyncio
import logging

from bot.plugins.base import BasePlugin


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    def on_message(self, message):
        if message.channel.name != 'developer':
            return

        if message.content.startswith('!'):
            for i in [1, 2, 5]:
                logger.debug('Sleeping for %d seconds', i)
                yield from asyncio.sleep(i)

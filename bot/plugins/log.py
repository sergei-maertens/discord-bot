import logging

from .base import BasePlugin

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    async def on_message(self, message):
        logger.info('Received message: %s', message.content)

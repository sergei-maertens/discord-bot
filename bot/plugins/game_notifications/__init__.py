import logging

from bot.plugins.base import BasePlugin


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    def on_message(self, message):
        import bpdb; bpdb.set_trace()

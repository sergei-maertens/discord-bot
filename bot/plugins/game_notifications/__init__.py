import logging

from bot.plugins.base import BasePlugin


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    def on_status(self, member, old_game, old_status):
        import bpdb; bpdb.set_trace()

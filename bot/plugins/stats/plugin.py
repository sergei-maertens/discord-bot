import logging

from bot.channels.models import Channel
from bot.plugins.base import BasePlugin
from bot.users.models import Member

from .models import LoggedMessage


logger = logging.getLogger(__name__)


class Plugin(BasePlugin):

    has_blocking_io = True

    def on_message(self, message):
        """
        Log the message in the db
        """
        super().on_message(self, message)

        import bpdb; bpdb.set_trace()

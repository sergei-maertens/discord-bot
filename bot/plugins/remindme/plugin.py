import re

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command


class Plugin(BasePlugin):

    has_blocking_io = True

    @command(pattern=re.compile(r'(?P<time>\w+) (?P<message>.*)', re.IGNORECASE))
    def remindme(self, command):
        yield from command.send_typing()
        timedelta = self.parse_delta(command.args.time)
        yield from command.reply("In {} - {}".format(timedelta, command.args.message))

    def parse_delta(self, delta_string):
        """
        Parse a string to a timedelta object.

        Examples:
            - 30m = timedelta(minutes=30)
            - 1h = timedelta(hours=1)
            - 2days4h30m = timedelta(days=2, hours=4, minutes=30)
            - 5year3months2days1hour = timedelta(days=365*5+31*3+2, hours=1)
        """

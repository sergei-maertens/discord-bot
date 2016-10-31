import re

from django.utils import timezone

import parsedatetime

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command


class Plugin(BasePlugin):

    has_blocking_io = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cal = parsedatetime.Calendar()

    @command(pattern=re.compile(r'(?P<time>(\d{1,2}[a-z]+\ )+)(?P<message>.*)', re.IGNORECASE),
             help="Store a message to be reminded of later, e.g. !remindme 2days 4hours do the laundry")
    def remindme(self, command):
        yield from command.send_typing()
        timestamp = self.parse_delta(command.args.time)
        yield from command.reply("At {} - {}".format(timestamp, command.args.message))

    def parse_delta(self, delta_string):
        """
        Parse a string to a timedelta object.

        Examples:
            - 30m = timedelta(minutes=30)
            - 1h = timedelta(hours=1)
            - 2days4h30m = timedelta(days=2, hours=4, minutes=30)
            - 5year3months2days1hour = timedelta(days=365*5+31*3+2, hours=1)
        """
        dt, parsed = self.cal.parseDT(delta_string.strip(), sourceTime=timezone.now(), tzinfo=timezone.utc)
        if not parsed:
            raise ValueError("Could not parse the time string")
        return dt

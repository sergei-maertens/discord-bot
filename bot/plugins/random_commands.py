import random

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command


class Plugin(BasePlugin):

    @command()
    def penis(self, command):
        """
        Draws an ASCII penis
        """
        length = random.choice(range(3, 15))
        yield from command.reply('8{length}>'.format(length='='*length))

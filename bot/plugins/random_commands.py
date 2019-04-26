import random
import re

from discord.utils import find

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command


class Plugin(BasePlugin):

    @command()
    def ping(self, command):
        yield from command.reply('pong')

    @command()
    def penis(self, command):
        """
        Draws an ASCII penis
        """
        length = random.choice(range(3, 15))
        yield from command.reply('8{length}D'.format(length='=' * length))

    @command()
    def benis(self, command):
        yield from self.penis(command)

    @command(pattern=re.compile(r'(?P<subject>.*)'))
    def whoinvented(self, command):
        guspetti = find(lambda m: m.id == '104532370899611648', command.message.server.members)
        yield from command.reply(
            "According to {guspetti}, {word} was invented by the Romans in Rome".format(
                guspetti=guspetti.mention,
                word=command.args.subject
            )
        )

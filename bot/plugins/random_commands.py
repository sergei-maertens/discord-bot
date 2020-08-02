import random
import re

from discord.utils import find

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command

GUS = 104532370899611648


class Plugin(BasePlugin):

    @command()
    async def ping(self, command):
        await command.reply('pong')

    @command()
    async def penis(self, command):
        """
        Draws an ASCII penis
        """
        length = random.choice(range(3, 15))
        await command.reply('8{length}D'.format(length='=' * length))

    @command()
    async def benis(self, command):
        await self.penis(command)

    @command(pattern=re.compile(r'(?P<subject>.*)'))
    async def whoinvented(self, command):
        guspetti = find(lambda m: m.id == GUS, command.message.server.members)
        await command.reply(
            "According to {guspetti}, {word} was invented by the Romans in Rome".format(
                guspetti=guspetti.mention,
                word=command.args.subject
            )
        )

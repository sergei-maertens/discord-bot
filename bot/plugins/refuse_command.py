import random

from bot.plugins.base import BasePlugin
from bot.plugins.events import command_resolved, receiver


class Plugin(BasePlugin):

    MESSAGES = [
        "Meh, maybe later",
        "I don't feel like it",
        "Go and ask someone else, I'm on my coffee break",
        "You again? Go annoy @Google or something",
        "Why don't you do something yourself for once?",
    ]

    @receiver(command_resolved)
    def refuse_command(self, command, handler):
        msg = random.choice(self.MESSAGES)
        yield from command.reply(msg)

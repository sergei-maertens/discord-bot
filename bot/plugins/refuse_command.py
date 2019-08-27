import random
import re

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command
from bot.plugins.events import StopCommandExecution, command_resolved, receiver
from bot.users.decorators import bot_admin_required

BASE_PROBABILITY = 0.1  # 10% to start with


class Plugin(BasePlugin):

    MESSAGES = [
        "Meh, maybe later",
        "I don't feel like it",
        "Go and ask someone else, I'm on my coffee break",
        "You again? Go annoy @Google or something",
        "Why don't you do something yourself for once?",
    ]

    PROBABILITY = BASE_PROBABILITY

    IGNORE_COMMANDS = [
        'reset probability',
    ]

    @receiver(command_resolved)
    async def refuse_command(self, command, handler):
        if random.random() < self.PROBABILITY and command.command.name not in self.IGNORE_COMMANDS:
            msg = random.choice(self.MESSAGES)
            await command.reply(msg)
            raise StopCommandExecution()

    @command(pattern=re.compile(r'(?P<prob>0\.[\d]+)'))
    async def set_probability(self, command):
        self.PROBABILITY = float(command.args.prob)
        await command.reply(f"Probability set to {self.PROBABILITY}")

    @command()
    async def show_probability(self, command):
        await command.reply("It's {0:.2%} likely that I'll refuse commands".format(self.PROBABILITY))

    @command()
    @bot_admin_required
    async def reset_probability(self, command):
        self.PROBABILITY = BASE_PROBABILITY
        await command.reply("Reset mutiny likelikehood to {0:.2%}".format(self.PROBABILITY))

    @command(pattern=re.compile(r'(?P<message>[\w\.!?,@<> ]+)'))
    async def add_mutiny_message(self, command):
        self.MESSAGES.append(command.args.message)
        await command.reply("Added `{}`".format(command.args.message))

import asyncio
import re


__all__ = ['PREFIX', 'command']


PREFIX = '!'


class command(object):

    """
    Decorator for command handlers in bot Plugins.
    """

    def __init__(self, name=None, pattern=None):
        assert not callable(name), 'You forgot the parentheses for the decorator'

        self.name = name
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.regex = pattern

    def __call__(self, func):
        """
        Decorator
        """
        if self.name is None:
            self.name = func.__name__
        func._command = self
        return func


class Args(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Command(object):

    for_message = None
    client = None

    def __init__(self, command, **kwargs):
        self.command = command
        self.args = Args(**kwargs)

    @property
    def message(self):
        return self.for_message

    @asyncio.coroutine
    def send_typing(self, dest=None):
        yield from self.client.send_typing(dest or self.for_message.channel)

    @asyncio.coroutine
    def reply(self, text):
        channel = self.for_message.channel
        yield from self.client.send_message(channel, text)

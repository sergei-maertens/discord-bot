import asyncio
import re


__all__ = ['PREFIX', 'command']


PREFIX = '!'


class command(object):

    """
    Decorator for command handlers in bot Plugins.
    """

    def __init__(self, name=None, pattern=None, help=None):
        assert not callable(name), 'You forgot the parentheses for the decorator'

        self.name = name
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.regex = pattern
        self.help = help

    def __call__(self, func):
        """
        Decorator
        """
        if self.name is None:
            self.name = func.__name__.replace('_', ' ')
        if self.help is None:
            self.help = func.__doc__.strip().split('\n')[0] if func.__doc__ else None
        func._command = self
        return func

    def as_help(self):
        cmd = "`{prefix}{name}{pattern}`".format(
            prefix=PREFIX,
            name=self.name,
            pattern=' {}'.format(self.regex.pattern) if self.regex else ''
        )
        return "{cmd}{spacer}{help}".format(cmd=cmd, help=self.help or '', spacer=' - ' if self.help else '')


class Args(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Command(object):

    for_message = None
    client = None

    def __init__(self, command, for_message=None, **kwargs):
        self.command = command
        self.args = Args(**kwargs)
        self.for_message = for_message

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

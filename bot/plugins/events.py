import asyncio
from functools import partial


class EventPool:

    def register(self, plugin):
        for event, handlers in plugin._event_handlers.items():
            handlers = [partial(handler, plugin) for handler in handlers]
            event.register(*handlers)


class Event:

    def __init__(self, name):
        self.name = name
        self.listeners = []

    def __repr__(self):
        return '<bot.plugins.events.Event name={0.name}>'.format(self)

    def register(self, *handlers):
        for handler in handlers:
            self.listeners.append(asyncio.coroutine(handler))

    @asyncio.coroutine
    def dispatch(self, *args, **kwargs):
        coros = [listener(*args, **kwargs) for listener in self.listeners]
        yield from asyncio.gather(*coros)


def receiver(event):
    def decorator(callback):
        # coro = asyncio.coroutine(callback)
        callback._event = event
        return callback
    return decorator


# built in events
command_resolved = Event('command_resolved')

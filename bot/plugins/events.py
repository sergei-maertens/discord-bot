import asyncio
from functools import partial


class EventPool:

    def register(self, plugin):
        for event, handlers in plugin._event_handlers.items():
            handlers = [partial(handler, plugin) for handler in handlers]
            event.register(*handlers)


class EventError(Exception):
    pass


class Event:

    def __init__(self, name=None):
        if name:
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
        results = yield from asyncio.gather(*coros, return_exceptions=True)
        exceptions = [result for result in results if isinstance(result, Exception)]
        return self.handle_exceptions(*exceptions)

    def handle_exceptions(self, *exceptions):
        if exceptions:
            raise EventError('Got %d unhandled exception(s)' % len(exceptions))


def receiver(event):
    def decorator(callback):
        # coro = asyncio.coroutine(callback)
        callback._event = event
        return callback
    return decorator


# built in events
class StopCommandExecution(Exception):
    pass


class CommandResolvedEvent(Event):
    name = 'command_resolved'

    def handle_exceptions(self, *exceptions):
        unexpected_exceptions = [exc for exc in exceptions if not isinstance(exc, StopCommandExecution)]
        super().handle_exceptions(*unexpected_exceptions)
        has_stop_command = len(exceptions) > len(unexpected_exceptions)
        return has_stop_command


command_resolved = CommandResolvedEvent()

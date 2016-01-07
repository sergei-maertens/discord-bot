import asyncio
import functools
import logging

from . import commands


logger = logging.getLogger(__name__)


class MethodPool(dict):

    # Track which handlers come from which plugin
    plugin_handlers = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_handlers = {}

    def register(self, plugin):
        """
        Take in the event handlers from a plugin and group them by event
        """
        for handler, method in plugin._callbacks.items():
            wrapped = plugin._wrap(method)
            self.add(handler, wrapped)
            self.plugin_handlers.setdefault(plugin, wrapped)
            logger.debug('Registered %r from %r', method, plugin)

    def add(self, name, handler):
        if name not in self:
            self[name] = []
        self[name].append(handler)

    def group(self, handlers):
        """
        Groups all handlers into one wrapping handler that distributes the event.

        This is where the 'magic' happens. A distinction is made between plugins
        and/or handlers that perform blocking IO (such as the reddit API wrapper,
        Django ORM, ...). Blocking handlers are executed in a loop executor (by
        default a thread pool), while real coroutines are just executed as-is.
        """

        def grouped(*args, **kwargs):
            coros = []
            for handler in handlers:
                if handler._has_blocking_io:
                    loop = self.client.loop
                    future = loop.run_in_executor(None, functools.partial(handler, *args, **kwargs))
                    coro = yield from future
                    coros.append(coro)
                else:
                    handler = asyncio.coroutine(handler)(*args, **kwargs)  # real coroutine can be called
                    coros.append(handler)
            yield from asyncio.gather(*coros)
        return grouped

    def bind_to(self, client):
        """
        Wraps all registered handlers in a function and binds it to the client.
        """
        self.client = client
        client._method_pool = self
        for event, handlers in self.items():
            grouper = self.group(handlers)
            grouper.__name__ = event
            client.async_event(grouper)


class BasePluginMeta(type):

    def __new__(mcs, name, bases, attrs):
        new_cls = super().__new__(mcs, name, bases, attrs)

        for attr, val in new_cls.__dict__.items():
            # check for direct event handlers
            if attr.startswith('on_'):
                new_cls._callbacks[attr] = val

            # register the plugin commands
            elif callable(val) and hasattr(val, '_command'):
                cmd = '{0}{1}'.format(commands.PREFIX, val._command.name)
                new_cls.commands[cmd] = asyncio.coroutine(val)

        return new_cls


class BasePlugin(object, metaclass=BasePluginMeta):

    has_blocking_io = False  # set to True to run events in an executor
    commands = {}
    _callbacks = {}

    def __init__(self, client, options):
        self.client = client
        self.options = options

    def _wrap(self, method):
        handler = functools.partial(method, self)
        handler.__name__ = method.__name__
        handler._has_blocking_io = self.has_blocking_io
        return handler

    def get_command(self, msg):
        """
        Get the command that matches with str:`msg`
        """
        for cmd, handler in self.commands.items():
            if msg.lower().startswith(cmd.lower()):

                # Simple command
                if handler._command.regex is None:
                    return handler

                # Regex matching, cut of the command part
                str_to_test = msg.replace(cmd, '', 1).strip()
                match = handler._command.regex.match(str_to_test)
                if not match:
                    continue

                command = commands.Command(handler._command, **match.groupdict())
                return handler, command
        return None

    def on_message(self, message):
        import bpdb; bpdb.set_trace()
        result = self.get_command(message.content)
        if result:
            handler, command = result
            command.for_message, command.client = message, self.client
            assert asyncio.iscoroutinefunction(handler)
            yield from handler(self, command)

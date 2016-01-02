import asyncio
import logging
import functools

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
        handlers = {}
        for attr, val in attrs.items():
            if attr.startswith('on_'):
                handlers[attr] = val
        attrs['_callbacks'] = handlers
        return super().__new__(mcs, name, bases, attrs)


class BasePlugin(object, metaclass=BasePluginMeta):

    has_blocking_io = False  # set to True to run events in an executor

    def __init__(self, client, options):
        self.client = client
        self.options = options

    def _wrap(self, method):
        handler = functools.partial(method, self)
        handler.__name__ = method.__name__
        handler._has_blocking_io = self.has_blocking_io
        return handler

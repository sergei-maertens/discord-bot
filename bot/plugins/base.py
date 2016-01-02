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
        def grouped(*args, **kwargs):
            for handler in handlers:
                yield from handler(*args, **kwargs)
            return
        return grouped

    def bind_to(self, client):
        """
        Wraps all registered handlers in a function and binds it to the client.
        """
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
        handler = asyncio.coroutine(functools.partial(method, self))
        handler.__name__ = method.__name__
        return handler

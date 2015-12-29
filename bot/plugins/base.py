import functools


class BasePluginMeta(type):

    def __new__(mcs, name, bases, attrs):
        handlers = {}
        for attr, val in attrs.items():
            if attr.startswith('on_'):
                handlers[attr] = val
        attrs['_callbacks'] = handlers
        return super().__new__(mcs, name, bases, attrs)


class BasePlugin(object, metaclass=BasePluginMeta):

    def __init__(self, client, options):
        self.client = client
        self.options = options

    def run(self):
        """
        Bind the events
        """
        for handler, method in self._callbacks.items():
            handler = functools.partial(method, self)
            handler.__name__ = method.__name__
            self.client.event(handler)

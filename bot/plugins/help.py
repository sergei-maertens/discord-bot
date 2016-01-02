from bot.plugins.base import BasePlugin


class Plugin(BasePlugin):

    def on_message(self, message):
        if message.content.lower() == '!help':
            plugins = self.client._method_pool.plugin_handlers.keys()
            help_messages = [plugin.help for plugin in plugins if hasattr(plugin, 'help')]
            msg = '\n\n'.join(help_messages)
            yield from self.client.send_message(message.channel, msg)

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command


class Plugin(BasePlugin):

    @command()
    def help(self, command):
        plugins = self.client._method_pool.plugin_handlers.keys()
        help_messages = [plugin.help for plugin in plugins if hasattr(plugin, 'help')]
        msg = '\n\n'.join(help_messages)
        yield from command.reply(msg)

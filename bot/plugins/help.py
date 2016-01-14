import re

from django.conf import settings
from django.utils.functional import cached_property

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command


class Plugin(BasePlugin):

    @cached_property
    def plugins(self):
        """
        Returns a list of enabled plugins
        """
        enabled = self.client._method_pool.plugin_handlers.keys()
        # strip off the 'plugin' bit if present (complex plugins)
        modules = [re.sub(r'\.plugin$', '', mod) for mod in enabled]
        names = [mod.split('.')[-1] for mod in modules]
        return names

    @command()
    def help(self, command):
        plugins = self.client._method_pool.plugin_handlers.keys()
        help_messages = [plugin.help for plugin in plugins if hasattr(plugin, 'help')]
        msg = '\n\n'.join(help_messages)
        yield from command.reply(msg)

    @command()
    def list_plugins(self, command):
        all_plugins = set(settings.PLUGINS)
        enabled = set(self.plugins)
        disabled = all_plugins ^ enabled

        msg = 'Enabled plugins: `{enabled}`\nDisabled plugins: `{disabled}`'.format(
            enabled='`, `'.join(enabled), disabled='`, `'.join(disabled)
        )
        yield from command.reply(msg)

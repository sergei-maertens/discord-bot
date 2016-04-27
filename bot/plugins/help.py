import re

from django.conf import settings
from django.utils.functional import cached_property

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command


def get_commands(plugin):
    commands = []
    for attr_name in dir(plugin):
        attr = getattr(plugin, attr_name)
        if hasattr(attr, '_command'):
            commands.append(attr._command)
    return commands


RE_PLUGIN = re.compile(r'\.plugin$')


def module_to_plugin_name(module):
    # strip off the 'plugin' bit if present (complex plugins)
    return re.sub(RE_PLUGIN, '', module).split('.')[-1]


class Plugin(BasePlugin):

    @cached_property
    def plugins(self):
        """
        Returns a list of enabled plugins
        """
        enabled = self.client._method_pool.plugin_modules.keys()
        return [module_to_plugin_name(mod) for mod in enabled]

    @command()
    def help(self, command):
        help_messages = []
        for module, plugin in self.client._method_pool.plugin_modules.items():
            if plugin is self:  # TODO: FIXME
                continue

            msgs = [cmd.as_help() for cmd in get_commands(plugin)]
            if not msgs:
                continue

            help_messages += [
                '**{plugin}**'.format(plugin=module_to_plugin_name(module))
            ] + msgs + ['']

        msg = '\n'.join(help_messages)
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

# -*- coding: utf-8 -*-
"""
Main entry point for the bot.

This module performs the start-up, login and reads out the settings to configure
the bot.
"""
import logging
from importlib import import_module

import discord

from bot import settings
from bot.utils import configure_logging

logger = logging.getLogger('bot')


client = discord.Client()


@client.event
def on_ready():
    logger.info('Logged in as %s', settings.EMAIL)


def main():
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
    logger.info('Starting up bot')

    # login
    client.login(settings.EMAIL, settings.PASSWORD)

    for plugin, options in settings.PLUGINS.items():
        _plugin = import_module('bot.plugins.%s' % plugin)
        plugin = _plugin.Plugin(client, options)
        plugin.run()
        logger.debug('Configured plugin %r', plugin)

    client.run()


if __name__ == '__main__':
    main()

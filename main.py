#!/usr/bin/env python
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
from bot.plugins.base import MethodPool
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
    if not settings.DEBUG:
        client.login(settings.EMAIL, settings.PASSWORD)

    pool = MethodPool()  # pool that holds all callbacks
    for plugin, options in settings.PLUGINS.items():
        _plugin = import_module('bot.plugins.%s' % plugin)
        plugin = _plugin.Plugin(client, options)
        pool.register(plugin)
        pool.bind_to(client)
        logger.debug('Configured plugin %r', plugin)

    if not settings.DEBUG:
        client.run()


if __name__ == '__main__':
    main()

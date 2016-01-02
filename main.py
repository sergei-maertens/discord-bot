#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main entry point for the bot.

This module performs the start-up, login and reads out the settings to configure
the bot.
"""
import logging
from importlib import import_module

import django
import discord

from django.conf import settings
from bot.plugins.base import MethodPool


logger = logging.getLogger('bot')

client = discord.Client()


@client.async_event
def on_ready():
    logger.info('Logged in as %s, id: %s', client.user.name, client.user.id)


def main():
    django.setup()  # configures logging etc.
    logger.info('Starting up bot')

    pool = MethodPool()  # pool that holds all callbacks
    for plugin, options in settings.PLUGINS.items():
        module = 'bot.plugins.%s' % plugin
        if module in settings.INSTALLED_APPS:
            module = '%s.plugin' % module
        _plugin = import_module(module)
        plugin = _plugin.Plugin(client, options)
        pool.register(plugin)
        pool.bind_to(client)
        logger.debug('Configured plugin %r', plugin)

    # login & start
    client.run(settings.EMAIL, settings.PASSWORD)


if __name__ == '__main__':
    main()

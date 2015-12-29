# -*- coding: utf-8 -*-
"""
Main entry point for the bot.

This module performs the start-up, login and reads out the settings to configure
the bot.
"""
import logging

import discord

from bot import settings
from bot.utils import configure_logging

logger = logging.getLogger('bot')


def main():
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
    logger.info('Starting up bot')

    # login
    client = discord.Client()
    client.login(settings.LOGIN, settings.PASSWORD)


if __name__ == '__main__':
    main()

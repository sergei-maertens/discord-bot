from django.apps import AppConfig


class StatsConfig(AppConfig):
    name = 'bot.plugins.stats'

    def ready(self):
        from . import signals  # noqa

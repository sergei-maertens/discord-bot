from django.db.models.signals import post_save
from django.dispatch import receiver

from bot.games.models import Game


@receiver(post_save, sender=Game, dispatch_uid='bot.plugins.stats.signals.game_became_alias')
def game_became_alias(sender, raw=False, instance=None, created=False, **kwargs):
    if raw:
        return

    if (created and instance.alias_for_id) or instance.alias_for_id != instance._old_alias_for_id:
        instance.gamesession_set.update(game=instance.alias_for)
        instance._old_alias_for_id = instance.alias_for_id

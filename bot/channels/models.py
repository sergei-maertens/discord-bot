from django.db import models
from django.utils.translation import ugettext_lazy as _


class ChannelQuerySet(models.QuerySet):

    def from_message(self, message):
        discord_id = message.channel.id
        channel, created = self.get_or_create(discord_id=discord_id, defaults={
            'name': message.channel.name
        })
        return channel


class Channel(models.Model):
    discord_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(_('name'), max_length=50)

    allow_nsfw = models.BooleanField(default=False)

    objects = ChannelQuerySet.as_manager()

    def __str__(self):
        return self.name

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Channel(models.Model):
    discord_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(_('name'), max_length=50)

    allow_nsfw = models.BooleanField(default=False)

    def __str__(self):
        return self.name

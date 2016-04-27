from django.db import models
from django.utils.translation import ugettext_lazy as _


class LowerCaseCharField(models.CharField):

    def to_python(self, value):
        value = super().to_python(value)
        return value.lower() if value else value


class RedditCommand(models.Model):
    command = LowerCaseCharField(_('command'), max_length=100, unique=True)
    subreddit = LowerCaseCharField(_('subreddit'), max_length=50)
    times_used = models.PositiveIntegerField(default=0)

    nsfw = models.BooleanField(default=False)

    class Meta:
        unique_together = ('command', 'subreddit')
        ordering = ['subreddit']

    def __str__(self):
        return '!{0.command} -> /r/{0.subreddit}'.format(self)

    def save(self, *args, **kwargs):
        self.command = self.command.lower()
        self.subreddit = self.subreddit.lower()
        super().save(*args, **kwargs)

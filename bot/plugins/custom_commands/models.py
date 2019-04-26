from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..commands import PREFIX


def no_prefix_at_beginning(value):
    if value.startswith(PREFIX):
        raise ValidationError(
            _("Provide the command without the prefix '%(prefix)s'"),
            code='prefix_present', params={'prefix': PREFIX}
        )


class Command(models.Model):
    command = models.CharField(
        _('command'), max_length=50,
        help_text=_('trigger for the command, e.g. \'benis\''),
        validators=[no_prefix_at_beginning]
    )
    description = models.CharField(_('description'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('command')
        verbose_name_plural = _('commands')

    def __str__(self):
        return "{}{}".format(PREFIX, self.command)


class CommandAction(models.Model):
    command = models.ForeignKey(Command)
    action = models.TextField(_('action'), help_text=_('Text to be replied'))

    class Meta:
        verbose_name = _('command action')
        verbose_name_plural = _('command actions')

    def __str__(self):
        return self.action[:30]

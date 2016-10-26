from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class GameQuerySet(models.QuerySet):

    def get_by_name(self, name):
        games = self.filter(
            models.Q(name__iexact=name) | models.Q(game__name__iexact=name),
            alias_for__isnull=True
        ).distinct()
        try:
            return games.get()
        except self.model.DoesNotExist:
            return self.create(name=name)


class Game(models.Model):
    name = models.CharField(_('name'), max_length=255)
    alias_for = models.ForeignKey('self', null=True, blank=True)

    objects = GameQuerySet.as_manager()

    class Meta:
        verbose_name = _('game')
        verbose_name_plural = _('games')

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_alias_for_id = self.alias_for_id

    def clean(self):
        if self.alias_for and self.alias_for.alias_for:
            raise ValidationError(_("Aliases can only span one level"))
        if self.alias_for and self.alias_for.name == self.name:
            raise ValidationError(_("An alias must have a different name"))

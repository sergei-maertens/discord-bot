from django.db import models


class MemberQuerySet(models.QuerySet):

    def from_message(self, message):
        discord_id = message.author.id
        member, created = self.get_or_create(discord_id=discord_id)
        return member

    def from_mentions(self, mentions):
        return [self.get_or_create(discord_id=member.id)[0] for member in mentions]


class Member(models.Model):
    discord_id = models.CharField(max_length=50, unique=True)

    can_admin_bot = models.BooleanField(default=False)

    objects = MemberQuerySet.as_manager()

    def __str__(self):
        return '<@{}>'.format(self.discord_id)

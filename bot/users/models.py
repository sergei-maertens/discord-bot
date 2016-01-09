from django.db import models


class Member(models.Model):
    discord_id = models.CharField(max_length=50)
    can_admin_bot = models.BooleanField(default=False)

    def __str__(self):
        return '<@{}>'.format(self.discord_id)

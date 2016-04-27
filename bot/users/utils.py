from django.conf import settings

from .models import Member


def is_bot_admin(message):
    """
    Takes a message and decides whether the author has admin status or not.
    """
    author_id = message.author.id
    qs = Member.objects.filter(discord_id=author_id, can_admin_bot=True)
    return author_id == settings.OWNER_ID or qs.exists()


def has_channel_permission(message, permission):
    author = message.author
    permissions = author.permissions_in(message.channel)
    return getattr(permissions, permission)

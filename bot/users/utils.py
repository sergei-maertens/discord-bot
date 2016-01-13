from .models import Member


def is_admin(self, message):
    """
    Takes a message and decides whether the author has admin status or not.
    """
    author_id = message.author.id
    qs = Member.objects.filter(discord_id=author_id, can_admin_bot=True)
    return author_id == self.options['owner_id'] or qs.exists()

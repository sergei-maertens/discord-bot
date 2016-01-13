from functools import wraps

from .utils import is_admin


def admin_required(func):
    """
    This decorator peforms database lookups, so if you use it,
    the plugin must be marked as ``has_blocking_io = True``.
    """

    @wraps(func)
    def decorator(plugin, command, *args, **kwargs):
        if not is_admin(command.message):
            yield from command.reply('You don\'t have permission for this command')
            return
        yield from func(plugin, command, *args, **kwargs)
    return decorator

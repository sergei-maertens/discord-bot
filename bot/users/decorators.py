from functools import wraps

from .utils import has_channel_permission, is_bot_admin


def command_passes_test(check_function, message='Insufficient permissions'):
    """
    Decorator factory that takes a function that tests the command for permission.
    """
    def decorator(func):
        @wraps(func)
        async def _wrapped(plugin, command, *args, **kwargs):
            if not check_function(command):
                await command.reply(message)
                return
            await func(plugin, command, *args, **kwargs)
        return _wrapped
    return decorator


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        async def _wrapped(plugin, command, *args, **kwargs):
            if not has_channel_permission(command.message, permission):
                await command.reply('Insufficient permissions: `{}` required'.format(permission))
                return
            await func(plugin, command, *args, **kwargs)
        return _wrapped
    return decorator


def bot_admin_required(func):
    """
    This decorator peforms database lookups, so if you use it,
    the plugin must be marked as ``has_blocking_io = True``.
    """

    @wraps(func)
    async def decorator(plugin, command, *args, **kwargs):
        if not is_bot_admin(command.message):
            await command.reply('You don\'t have permission for this command')
            return
        await func(plugin, command, *args, **kwargs)
    return decorator

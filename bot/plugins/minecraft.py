import re

from mcrcon import MCRcon

from bot.plugins.base import BasePlugin
from bot.plugins.commands import command
from bot.users.decorators import bot_admin_required


class Plugin(BasePlugin):
    has_blocking_io = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = self.options["server"]
        self.password = self.options["password"]

    @command(
        pattern=re.compile(r"(?P<cmd>/?.+)"),
        help="Execute the command to the minecraft server"
    )
    @bot_admin_required
    async def mc(self, command):
        cmd = command.args.cmd
        if not cmd.startswith("/"):
            cmd = f"/{cmd}"

        with MCRcon(self.server, self.password) as mcr:
            resp = mcr.command(cmd)

        lines = resp.split("\n")
        resp = "\n".join([f"> {line}" for line in lines])

        await command.reply(resp)

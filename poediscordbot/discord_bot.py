import discord
from discord.ext import commands
from discord.ext.commands import bot
from instance import config

from poediscordbot.cogs.pob.pob_cog import PoBCog
from poediscordbot.cogs.sync.sync_cog import SyncCog
from poediscordbot.util.logging import log


class PobBot(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents(message_content=True, messages=True, guilds=True, dm_messages=True)
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=False, intents=intents)
        self.owner_ids = config.owners
        self.remove_command('help')

    async def on_ready(self):
        await self.add_cog(PoBCog(bot, config.active_channels, config.allow_pming))
        await self.add_cog(SyncCog(self))
        log.info(f'Logged in: uname={self.user.name}, id={self.user.id}')
        if config.presence_message:
            await self.change_presence(activity=discord.Activity(name=config.presence_message))

        synced_commands = await self.tree.fetch_commands()
        available_commands = self.tree.get_commands()

        if self.commands_differ(available_commands, synced_commands):
            log.info("Trying to sync command tree globally")
            cmds = await self.tree.sync()
            command_names = self.get_command_names(cmds)
            log.info(f"commands [{command_names}] from tree synced")

    @staticmethod
    def commands_differ(available_commands, synced_commands):
        local = set(PobBot.get_command_names(available_commands))
        synced = set(PobBot.get_command_names(synced_commands))
        return len(local.symmetric_difference(synced)) > 0

    @staticmethod
    def get_command_names(cmds):
        return [c.name for c in cmds]
